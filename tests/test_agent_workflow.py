"""Production workflow tests spanning agents, schemas, API, and MCP routes."""

from copy import deepcopy

from fastapi.testclient import TestClient

from app.agents import CareerAdvisorAgent
from app.main import app
from app.schemas import AgentRecommendationResponse
from app.tools.safety_tools import get_safety_notice

client = TestClient(app)


def profile_payload() -> dict[str, object]:
    return {
        "name": "Evaluation User",
        "education": "Final-year IT student",
        "interests": ["AI", "web development", "product building"],
        "skills": ["Python", "React", "SQL"],
        "career_goal": "Become an AI full-stack developer",
        "preferred_learning_style": "project_based",
        "language": "en",
        "experience_level": "university",
        "time_budget_hours_per_week": 8,
    }


def test_agent_returns_full_valid_response() -> None:
    response = CareerAdvisorAgent().run(profile_payload())
    validated = AgentRecommendationResponse.model_validate(response)

    assert len(validated.top_recommendations) >= 3
    assert validated.safety_notice == get_safety_notice()
    assert validated.skill_gap
    assert validated.personalized_roadmap


def test_recommendations_have_bounded_scores_and_reasons() -> None:
    response = CareerAdvisorAgent().run(profile_payload())

    for recommendation in response["top_recommendations"]:
        assert 0 <= recommendation["score"] <= 100
        assert recommendation["matched_reasons"]


def test_skill_gap_and_roadmap_contracts_are_complete() -> None:
    response = CareerAdvisorAgent().run(profile_payload())
    gap = response["skill_gap"]
    roadmap = response["personalized_roadmap"]

    assert {"matched_skills", "missing_skills", "priority_skills", "readiness_score"} <= gap.keys()
    assert 0 <= gap["readiness_score"] <= 100
    assert len(roadmap["thirty_day_plan"]) == 4
    assert len(roadmap["eight_week_plan"]) == 8


def test_agent_is_deterministic_and_does_not_mutate_input() -> None:
    profile = profile_payload()
    original = deepcopy(profile)
    agent = CareerAdvisorAgent()

    assert agent.run(profile) == agent.run(profile)
    assert profile == original


def test_recommend_api_supports_top_k_and_validation() -> None:
    response = client.post("/recommend?top_k=5", json=profile_payload())

    assert response.status_code == 200
    assert len(response.json()["top_recommendations"]) == 5
    assert client.post("/recommend", json=profile_payload() | {"skills": []}).status_code == 422


def test_existing_health_metadata_and_mcp_routes_work() -> None:
    assert client.get("/").status_code == 200
    assert client.get("/metadata").status_code == 200
    assert client.get("/tools").status_code == 200
    assert client.get("/mcp/careers?limit=2").status_code == 200
    assert client.get("/mcp/skills?limit=2").status_code == 200
