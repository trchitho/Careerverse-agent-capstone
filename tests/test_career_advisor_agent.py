"""Tests for the complete multi-agent career advisor workflow."""

from copy import deepcopy

import pytest

from app.agents import CareerAdvisorAgent
from app.schemas.profile_schema import AgentRecommendationResponse, UserProfileRequest


def valid_profile() -> dict[str, object]:
    return {
        "name": "Tho",
        "education": "Final-year IT student",
        "interests": ["AI", "web development"],
        "skills": ["Python", "React", "SQL"],
        "career_goal": "Become an AI full-stack developer",
    }


def test_valid_dict_profile_returns_full_response() -> None:
    response = CareerAdvisorAgent().run(valid_profile())

    assert response["user_summary"]["name"] == "Tho"
    assert response["top_recommendations"]
    assert response["skill_gap"]
    assert response["personalized_roadmap"]
    assert response["safety_notice"]
    assert response["course_concepts_demonstrated"]
    AgentRecommendationResponse.model_validate(response)


def test_pydantic_profile_and_top_k_five_are_supported() -> None:
    profile = UserProfileRequest.model_validate(valid_profile())

    response = CareerAdvisorAgent().run(profile, top_k=5)

    assert len(response["top_recommendations"]) == 5
    AgentRecommendationResponse.model_validate(response)


def test_advisor_is_deterministic_and_does_not_mutate_input() -> None:
    profile = valid_profile()
    before = deepcopy(profile)
    agent = CareerAdvisorAgent()

    first = agent.run(profile)
    second = agent.run(profile)

    assert first == second
    assert profile == before


def test_invalid_profile_raises_safe_value_error() -> None:
    with pytest.raises(ValueError, match="Profile is invalid"):
        CareerAdvisorAgent().run({})


def test_top_recommendation_drives_gap_and_roadmap() -> None:
    response = CareerAdvisorAgent().run(valid_profile())
    top = response["top_recommendations"][0]
    gap = response["skill_gap"]
    roadmap = response["personalized_roadmap"]

    assert roadmap["career_id"] == top["career_id"]
    assert set(gap["matched_skills"]).issubset(set(top["required_skills"]))
    required_or_optional = {
        *top["required_skills"],
        *top["nice_to_have_skills"],
    }
    assert set(gap["missing_skills"]).issubset(required_or_optional)


def test_invalid_top_k_is_reported_safely() -> None:
    with pytest.raises(ValueError, match="top_k"):
        CareerAdvisorAgent().run(valid_profile(), top_k=0)
