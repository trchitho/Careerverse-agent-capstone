"""Tests for the repository layer implementations."""

from __future__ import annotations

import pytest

from app.core.exceptions import ResourceNotFoundError
from app.repositories.career_repository import JsonCareerRepository
from app.repositories.roadmap_repository import JsonRoadmapRepository
from app.repositories.skill_repository import JsonSkillRepository
from app.tools.career_tools import recommend_careers


def test_career_repository_list_and_get() -> None:
    repo = JsonCareerRepository()
    careers = repo.list_careers()
    assert isinstance(careers, list)
    assert len(careers) > 0

    first_career = careers[0]
    career_id = first_career["id"]
    fetched = repo.get_career_by_id(career_id)
    assert fetched["id"] == career_id
    assert fetched["title"] == first_career["title"]


def test_career_repository_missing_raises_error() -> None:
    repo = JsonCareerRepository()
    with pytest.raises(ResourceNotFoundError, match="not found"):
        repo.get_career_by_id("non_existent_career_id_123")


def test_career_repository_search() -> None:
    repo = JsonCareerRepository()
    results = repo.search_careers("AI")
    assert isinstance(results, list)
    # Search is case-insensitive
    results_lower = repo.search_careers("ai")
    assert len(results) == len(results_lower)


def test_skill_repository_list_and_get() -> None:
    repo = JsonSkillRepository()
    skills = repo.list_skills()
    assert isinstance(skills, list)
    assert len(skills) > 0

    first_skill = skills[0]
    skill_name = first_skill["name"]
    fetched = repo.get_skill_by_name(skill_name)
    assert fetched["id"] == first_skill["id"]
    assert fetched["name"] == skill_name


def test_skill_repository_alias_lookup() -> None:
    repo = JsonSkillRepository()
    # Find a skill with aliases
    skill_with_alias = None
    for skill in repo.list_skills():
        if skill.get("aliases"):
            skill_with_alias = skill
            break

    if skill_with_alias:
        alias = skill_with_alias["aliases"][0]
        fetched = repo.get_skill_by_name(alias)
        assert fetched["name"] == skill_with_alias["name"]


def test_roadmap_repository_list_and_get() -> None:
    repo = JsonRoadmapRepository()
    roadmaps = repo.list_roadmaps()
    assert isinstance(roadmaps, dict)
    assert len(roadmaps) > 0

    career_id = next(iter(roadmaps.keys()))
    fetched = repo.get_roadmap_by_career_id(career_id)
    assert fetched == roadmaps[career_id]


def test_roadmap_repository_missing_raises_error() -> None:
    repo = JsonRoadmapRepository()
    with pytest.raises(ResourceNotFoundError, match="not found"):
        repo.get_roadmap_by_career_id("non_existent_career_id_123")


def test_repositories_do_not_mutate_dataset() -> None:
    # Mutating returned record should not alter cached values
    repo = JsonCareerRepository()
    first = repo.list_careers()[0]
    original_title = first["title"]
    first["title"] = "MUTATED"
    assert repo.list_careers()[0]["title"] == original_title


def test_recommend_careers_still_works() -> None:
    profile = {
        "interests": ["AI"],
        "skills": ["Python"],
        "career_goal": "Become an AI full-stack developer",
    }
    results = recommend_careers(profile, top_k=3)
    assert len(results) == 3
