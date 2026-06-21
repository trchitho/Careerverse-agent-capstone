"""Tests for saved recommendations endpoints and storage services."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.saved_recommendation_service import _session_repo

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clear_session_store() -> None:
    _session_repo.clear()


def test_saved_recommendations_flow_and_api() -> None:
    # 1. Generate recommendation
    profile = {
        "name": "Jane Doe",
        "education": "IT Student",
        "interests": ["AI"],
        "skills": ["Python"],
        "career_goal": "Become an AI full-stack developer",
    }
    rec_res = client.post("/api/v1/recommend", json=profile)
    assert rec_res.status_code == 200
    rec_data = rec_res.json()

    # 2. Save recommendation via API
    save_payload = {
        "session_id": "session-12345",
        "recommendation_response": rec_data,
    }
    save_res = client.post("/api/v1/recommendations/save", json=save_payload)
    assert save_res.status_code == 200

    saved_item = save_res.json()
    assert saved_item["session_id"] == "session-12345"
    assert saved_item["career_title"] == rec_data["top_recommendations"][0]["title"]
    assert "safety_notice" in saved_item
    assert "summary" in saved_item
    assert "id" in saved_item

    # 3. Retrieve saved recommendations via API
    list_res = client.get("/api/v1/recommendations/saved/session-12345")
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) == 1
    assert items[0]["id"] == saved_item["id"]


def test_list_unknown_session_returns_empty_list() -> None:
    res = client.get("/api/v1/recommendations/saved/session-not-exist")
    assert res.status_code == 200
    assert res.json() == []


def test_blank_session_id_is_rejected() -> None:
    res = client.get("/api/v1/recommendations/saved/%20")
    # FastAPI returns 400 or raises bad request
    assert res.status_code in (400, 422)


def test_save_endpoint_handles_missing_fields() -> None:
    res = client.post(
        "/api/v1/recommendations/save",
        json={"session_id": "s1", "recommendation_response": {}},
    )
    assert res.status_code == 400
    assert "No recommendations found" in res.json()["detail"]


def test_existing_recommend_endpoint_remains_unaffected() -> None:
    profile = {
        "name": "Jane",
        "education": "University",
        "interests": ["AI"],
        "skills": ["Python"],
        "career_goal": "AI developer",
    }
    res = client.post("/api/v1/recommend", json=profile)
    assert res.status_code == 200
    assert "top_recommendations" in res.json()
