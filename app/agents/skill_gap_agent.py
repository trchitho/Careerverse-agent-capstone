"""Deterministic skill gap analysis agent."""

from app.schemas.profile_schema import SkillGapResult
from app.tools.career_tools import (
    calculate_missing_skills,
    calculate_skill_score,
    canonicalize_skill_names,
    normalize_list,
    normalize_text,
)


class SkillGapAgent:
    """Compare user skills with one career's skill requirements."""

    def analyze(
        self,
        user_skills: list[str],
        required_skills: list[str],
        nice_to_have_skills: list[str] | None = None,
        max_priority_skills: int = 5,
    ) -> dict[str, object]:
        """Return an ordered, schema-validated skill gap result."""
        if max_priority_skills < 0:
            raise ValueError("max_priority_skills must be non-negative")
        required = normalize_list(required_skills)
        if not required:
            return SkillGapResult(
                matched_skills=[],
                missing_skills=[],
                priority_skills=[],
                readiness_score=0.0,
            ).model_dump()
