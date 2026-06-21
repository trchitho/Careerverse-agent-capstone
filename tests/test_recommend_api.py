"""API tests for the production multi-agent recommendation endpoint."""

from fastapi.testclient import TestClient

import app.main as main_module

client = TestClient(main_module.app)


def valid_payload() -> dict[str, object]:
    return {
        "name": "Tho",
        "education": "Final-year IT student",
        "interests": ["AI", "web development"],
        "skills": ["Python", "React", "SQL"],
        "career_goal": "Become an AI full-stack developer",
    }


def test_recommend_returns_complete_response() -> None:
    response = client.post("/recommend", json=valid_payload())

    assert response.status_code == 200
    body = response.json()
    assert len(body["top_recommendations"]) == 3
    assert body["skill_gap"]
    assert len(body["personalized_roadmap"]["thirty_day_plan"]) == 4
    assert body["safety_notice"]
