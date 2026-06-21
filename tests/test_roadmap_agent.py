"""Tests for roadmap retrieval and fallback behavior."""

from copy import deepcopy

from app.agents import RoadmapAgent
from app.schemas.profile_schema import RoadmapResult


def test_load_roadmaps_returns_non_empty_dict() -> None:
    roadmaps = RoadmapAgent().load_roadmaps()

    assert isinstance(roadmaps, dict)
    assert roadmaps


def test_existing_career_returns_complete_roadmap() -> None:
    agent = RoadmapAgent()
    career_id = next(iter(agent.load_roadmaps()))

    roadmap = agent.get_roadmap(career_id)

    assert roadmap["career_id"] == career_id
    assert len(roadmap["thirty_day_plan"]) == 4
    assert len(roadmap["eight_week_plan"]) == 8
    RoadmapResult.model_validate(roadmap)


def test_missing_skills_are_added_to_prerequisites() -> None:
    agent = RoadmapAgent()
    career_id = next(iter(agent.load_roadmaps()))

    roadmap = agent.get_roadmap(career_id, missing_skills=["Docker", "FastAPI"])

    assert roadmap["prerequisites"][:2] == ["Docker", "FastAPI"]
