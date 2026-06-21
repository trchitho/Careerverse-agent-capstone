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
