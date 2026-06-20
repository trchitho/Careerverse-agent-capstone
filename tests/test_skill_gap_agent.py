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
