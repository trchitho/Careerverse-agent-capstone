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
        required_missing = calculate_missing_skills(user_skills, required)
        missing_keys = {normalize_text(skill) for skill in required_missing}
        matched = [
            skill for skill in required if normalize_text(skill) not in missing_keys
        ]
        optional_missing = calculate_missing_skills(user_skills, nice_to_have_skills)
        missing = normalize_list([*required_missing, *optional_missing])
        priorities = required_missing[:max_priority_skills]

        if len(priorities) < max_priority_skills:
            known = {normalize_text(skill) for skill in priorities}
            for skill in optional_missing:
                key = normalize_text(canonicalize_skill_names([skill])[0])
                if key not in known:
                    priorities.append(skill)
                    known.add(key)
                if len(priorities) == max_priority_skills:
                    break

        result = SkillGapResult(
            matched_skills=matched,
            missing_skills=missing,
            priority_skills=priorities,
            readiness_score=calculate_skill_score(user_skills, required),
        )
        return result.model_dump()
