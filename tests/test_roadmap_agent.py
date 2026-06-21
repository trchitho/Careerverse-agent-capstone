"""Tests for roadmap retrieval and fallback behavior."""

from copy import deepcopy

import pytest

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


def test_unknown_career_returns_schema_valid_fallback() -> None:
    roadmap = RoadmapAgent().get_roadmap(
        "future_role",
        "Future Role",
        ["Python", "Documentation"],
    )

    assert roadmap["career_id"] == "future_role"
    assert roadmap["career_title"] == "Future Role"
    assert len(roadmap["thirty_day_plan"]) == 4
    assert len(roadmap["eight_week_plan"]) == 8
    assert roadmap["safety_note"]
    RoadmapResult.model_validate(roadmap)


def test_fallback_includes_priority_skills_safely() -> None:
    roadmap = RoadmapAgent().get_roadmap(
        "new_role",
        missing_skills=["Python", "FastAPI"],
    )

    assert roadmap["prerequisites"][:2] == ["Python", "FastAPI"]
    assert "Python" in roadmap["thirty_day_plan"][0]["skills_practiced"]


def test_blank_career_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="career_id"):
        RoadmapAgent().get_roadmap("   ")


def test_cached_roadmap_data_is_not_mutated() -> None:
    agent = RoadmapAgent()
    career_id = next(iter(agent.load_roadmaps()))
    before = deepcopy(agent.load_roadmaps()[career_id])

    personalized = agent.get_roadmap(career_id, missing_skills=["Docker"])
    personalized["prerequisites"].append("Changed locally")

    assert agent.load_roadmaps()[career_id] == before
