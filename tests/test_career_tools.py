"""Offline tests for deterministic career recommendation tools."""

from copy import deepcopy

import pytest

from app.schemas.profile_schema import UserProfileRequest
from app.tools.career_tools import (
    calculate_goal_score,
    calculate_interest_score,
    calculate_skill_score,
    load_careers,
    load_skill_alias_index,
    load_skills,
    normalize_list,
    normalize_text,
    recommend_careers,
)


def sample_profile() -> dict[str, object]:
    return {
        "interests": ["AI", "web development"],
        "skills": ["Python", "React", "SQL"],
        "career_goal": "Become an AI full-stack developer",
    }


def test_load_careers_returns_non_empty_list() -> None:
    assert isinstance(load_careers(), list)
    assert load_careers()


def test_load_skills_returns_non_empty_list() -> None:
    assert isinstance(load_skills(), list)
    assert load_skills()
