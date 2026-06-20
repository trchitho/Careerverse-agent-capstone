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


def test_skill_score_exact_and_case_insensitive_match() -> None:
    score = calculate_skill_score(["python", "REACT"], ["Python", "React", "SQL"])

    assert score == pytest.approx(66.67)


def test_skill_score_alias_match_if_alias_exists() -> None:
    alias_index = load_skill_alias_index()
    alias = next(
        (
            key
            for key, canonical in alias_index.items()
            if normalize_text(key) != normalize_text(canonical)
        ),
        None,
    )
    if alias is None:
        pytest.skip("The generated dataset contains no distinct skill alias")
    canonical = alias_index[alias]

    assert calculate_skill_score([alias], [canonical]) == 100.0


def test_skill_score_empty_inputs_and_duplicates() -> None:
    assert calculate_skill_score([], ["Python"]) == 0.0
    assert calculate_skill_score(["Python"], []) == 0.0
    assert calculate_skill_score(["Python", "python"], ["Python", "SQL"]) == 50.0


def test_goal_score_matches_title_or_description() -> None:
    career = {
        "title": "Backend Developer",
        "description": "Build reliable Python API services",
        "family": "Software Engineering",
        "recommended_for": ["backend systems"],
    }

    assert calculate_goal_score("Build backend Python APIs", career) > 0


def test_goal_score_empty_or_unicode_goal_is_safe() -> None:
    career = {"title": "Data Analyst", "recommended_for": ["data analysis"]}

    assert calculate_goal_score("", career) == 0.0
    assert 0 <= calculate_goal_score("Phân tích dữ liệu cho giáo dục", career) <= 100


def test_recommend_careers_returns_top_three() -> None:
    results = recommend_careers(sample_profile())

    assert len(results) == 3
    assert all(0 <= item["score"] <= 100 for item in results)


def test_recommend_careers_top_k_five() -> None:
    assert len(recommend_careers(sample_profile(), top_k=5)) == 5


@pytest.mark.parametrize("top_k", [0, 21, 100])
def test_recommend_careers_top_k_bounds(top_k: int) -> None:
    with pytest.raises(ValueError, match="top_k"):
        recommend_careers(sample_profile(), top_k=top_k)


def test_recommend_careers_is_deterministic() -> None:
    first = recommend_careers(sample_profile(), top_k=10)
    second = recommend_careers(sample_profile(), top_k=10)

    assert first == second


def test_recommendations_are_sorted_by_score() -> None:
    results = recommend_careers(sample_profile(), top_k=20)
    scores = [item["score"] for item in results]

    assert scores == sorted(scores, reverse=True)


def test_recommendation_contains_explainable_fields() -> None:
    result = recommend_careers(sample_profile(), top_k=1)[0]

    assert set(result["score_breakdown"]) == {
        "interest_score", "skill_score", "goal_score", "weights"
    }
    assert result["matched_reasons"]
    assert len(result["missing_skills_preview"]) <= 8
    assert result["safety_note"]
