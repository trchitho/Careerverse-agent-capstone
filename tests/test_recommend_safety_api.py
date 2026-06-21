"""API regression tests for the recommendation safety boundary."""

from fastapi.testclient import TestClient

import app.main as main_module
from app.tools.safety_tools import get_safety_notice

client = TestClient(main_module.app)


def valid_payload() -> dict[str, object]:
    return {
        "name": "Demo User",
        "education": "Final-year IT student",
        "interests": ["AI", "web development"],
        "skills": ["Python", "React", "SQL"],
        "career_goal": "Become an AI full-stack developer",
        "preferred_learning_style": "project_based",
        "language": "en",
        "experience_level": "university",
        "time_budget_hours_per_week": 8,
    }


def test_normal_recommendation_keeps_exact_safety_notice() -> None:
    response = client.post("/recommend", json=valid_payload())

    assert response.status_code == 200
    assert response.json()["safety_notice"] == get_safety_notice()
