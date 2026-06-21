"""Tests for deterministic skill gap analysis."""

from copy import deepcopy

from app.agents import SkillGapAgent
from app.tools.career_tools import load_skill_alias_index, normalize_text


def test_exact_and_case_insensitive_skill_match() -> None:
    result = SkillGapAgent().analyze(
        ["python", "REACT"],
        ["Python", "React", "SQL"],
    )

    assert result["matched_skills"] == ["Python", "React"]
    assert result["missing_skills"] == ["SQL"]
    assert result["readiness_score"] == 66.67


def test_alias_match_if_dataset_has_alias() -> None:
    aliases = load_skill_alias_index()
    alias = next(
        (
            key
            for key, canonical in aliases.items()
            if normalize_text(key) != normalize_text(canonical)
        ),
        None,
    )
    assert alias is not None
    canonical = aliases[alias]

    result = SkillGapAgent().analyze([alias], [canonical])

    assert result["matched_skills"] == [canonical]
    assert result["readiness_score"] == 100.0


def test_missing_and_priority_skills_preserve_order() -> None:
    result = SkillGapAgent().analyze(
        ["Python"],
        ["Python", "FastAPI", "Docker", "SQL"],
        max_priority_skills=2,
    )

    assert result["missing_skills"] == ["FastAPI", "Docker", "SQL"]
    assert result["priority_skills"] == ["FastAPI", "Docker"]


def test_nice_to_have_skills_fill_priority_slots() -> None:
    result = SkillGapAgent().analyze(
        ["Python"],
        ["Python", "FastAPI"],
        ["Docker", "Cloud Run"],
        max_priority_skills=3,
    )

    assert result["missing_skills"] == ["FastAPI", "Docker", "Cloud Run"]
    assert result["priority_skills"] == ["FastAPI", "Docker", "Cloud Run"]


def test_empty_required_skills_are_safe() -> None:
    result = SkillGapAgent().analyze(["Python"], [], ["Docker"])

    assert result == {
        "matched_skills": [],
        "missing_skills": [],
        "priority_skills": [],
        "readiness_score": 0.0,
    }


def test_duplicate_user_skills_do_not_double_count() -> None:
    result = SkillGapAgent().analyze(
        ["Python", "python", "PYTHON"],
        ["Python", "SQL"],
    )

    assert result["matched_skills"] == ["Python"]
    assert result["readiness_score"] == 50.0


def test_inputs_are_not_mutated() -> None:
    user = ["Python"]
    required = ["Python", "SQL"]
    optional = ["Docker"]
    before = deepcopy((user, required, optional))

    SkillGapAgent().analyze(user, required, optional)

    assert (user, required, optional) == before


def test_readiness_score_stays_in_range() -> None:
    result = SkillGapAgent().analyze(["Python"], ["Python", "SQL"])

    assert 0 <= result["readiness_score"] <= 100
