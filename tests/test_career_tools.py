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


def test_normalize_text_handles_case_spaces_and_unicode() -> None:
    assert normalize_text("  C++   và  Node.js  ") == "c++ và node.js"


def test_normalize_list_deduplicates_case_insensitive() -> None:
    values = normalize_list([" Python ", "python", "  C#  ", "", "c#"])

    assert values == ["Python", "C#"]


def test_interest_score_exact_match() -> None:
    assert calculate_interest_score(["AI"], ["ai", "automation"]) == 100.0


def test_interest_score_empty_inputs() -> None:
    assert calculate_interest_score([], ["AI"]) == 0.0
    assert calculate_interest_score(["AI"], []) == 0.0


def test_interest_score_is_case_insensitive_and_deduplicated() -> None:
    score = calculate_interest_score(["AI", " ai "], ["Ai"])

    assert score == 100.0
