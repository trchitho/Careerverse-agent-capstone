"""Tests for API Versioning compatibility and structure."""

from __future__ import annotations

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

PROFILE = {
    "name": "Demo User",
    "education": "Final-year IT student",
    "interests": ["AI", "web development"],
    "skills": ["Python", "React"],
    "career_goal": "Become an AI full-stack developer",
    "preferred_learning_style": "project_based",
    "language": "en",
    "experience_level": "university",
    "time_budget_hours_per_week": 8,
}


def test_legacy_endpoints_compatibility() -> None:
    """Verify that legacy endpoints still function properly."""
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "ok" in res_root.json()["status"]

    res_recommend = client.post("/recommend", json=PROFILE)
    assert res_recommend.status_code == 200
    assert "top_recommendations" in res_recommend.json()
