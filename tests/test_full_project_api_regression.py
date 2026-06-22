"""Full project API boundary regression tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_not_found_endpoint() -> None:
    res = client.get("/api/v1/non-existent-route")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_api_recommendation_bounds() -> None:
    payload = {
        "name": "Jane",
        "education": "IT student",
        "interests": ["Coding"],
        "skills": ["Python"],
        "career_goal": "Goal"
    }
    # Ge boundary check for top_k (top_k=0 is ge=1 invalid)
    res = client.post("/api/v1/recommend?top_k=0", json=payload)
    assert res.status_code == 422
    
    # Le boundary check for top_k (top_k=11 is le=10 invalid)
    res = client.post("/api/v1/recommend?top_k=11", json=payload)
    assert res.status_code == 422


def test_api_invalid_json_payload() -> None:
    # Send malformed raw JSON
    res = client.post(
        "/api/v1/recommend",
        content="{malformed_json: true}",
        headers={"Content-Type": "application/json"}
    )
    assert res.status_code == 422
    assert "detail" in res.json()


def test_api_feedback_content_length_bounds() -> None:
    # Comments exceeding 300 character constraints
    feedback_payload = {
        "recommendation_id": "rec-01",
        "rating": 5,
        "comment": "A" * 301
    }
    res = client.post("/api/v1/feedback/recommendation", json=feedback_payload)
    assert res.status_code == 422
