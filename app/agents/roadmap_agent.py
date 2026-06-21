"""Roadmap retrieval and safe fallback agent."""

import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.repositories.roadmap_repository import JsonRoadmapRepository
from app.schemas.profile_schema import RoadmapResult
from app.tools.career_tools import normalize_list

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "roadmaps.json"
ROADMAP_SAFETY_NOTE = (
    "This roadmap is educational guidance only and should be adapted to the "
    "learner's context."
)

_roadmap_repo = JsonRoadmapRepository()


class RoadmapAgent:
    """Retrieve production roadmaps and produce schema-valid fallbacks."""

    @staticmethod
    def load_roadmaps() -> dict[str, dict[str, Any]]:
        """Load the local roadmap catalog using the repository layer."""
        return _roadmap_repo.list_roadmaps()

    @staticmethod
    def _fallback_week(
        week: int,
        career_title: str,
        priority_skills: list[str],
        phase: str,
    ) -> dict[str, object]:
        """Build one conservative fallback roadmap week."""
        first = priority_skills[(week - 1) % len(priority_skills)]
        second = priority_skills[week % len(priority_skills)]
        return {
            "week": week,
            "focus": f"{phase}: {career_title} foundations",
            "learning_goals": [
                f"Understand how {first} supports this career path",
                f"Practice {second} in a small guided exercise",
            ],
            "tasks": [
                f"Complete a focused {first} learning activity",
                f"Build a small exercise using {second}",
                "Review the result and document remaining questions",
            ],
            "deliverable": f"A documented week {week} learning artifact",
            "skills_practiced": [first, second],
            "checkpoint": "The learner can explain the work and identify a next step.",
        }

    def _build_fallback(
        self,
        career_id: str,
        career_title: str,
        missing_skills: list[str] | None,
    ) -> dict[str, object]:
        """Build a complete educational fallback for an unknown career."""
        priorities = normalize_list(missing_skills)[:5] or [
            "Problem Framing",
            "Learning Planning",
        ]
        short_phases = [
            "Foundations", "Guided practice", "Project application", "Portfolio review"
        ]
        long_phases = [
            "Orientation", "Foundations", "Guided practice", "Applied practice",
            "Quality review", "Project build", "Iteration", "Portfolio presentation",
        ]
        thirty_day = [
            self._fallback_week(week, career_title, priorities, phase)
            for week, phase in enumerate(short_phases, start=1)
        ]
        eight_week = [
            self._fallback_week(week, career_title, priorities, phase)
            for week, phase in enumerate(long_phases, start=1)
        ]
        return {
            "career_title": career_title,
            "career_id": career_id,
            "duration_options": ["30 days", "8 weeks"],
            "prerequisites": priorities,
            "thirty_day_plan": thirty_day,
            "eight_week_plan": eight_week,
            "recommended_mini_project": {
                "title": f"{career_title} Foundations Project",
                "description": (
                    "Build a small project that demonstrates the selected priority skills."
                ),
                "core_features": [
                    "A documented user goal",
                    "A working learning artifact",
                    "Validation notes and limitations",
                ],
                "stretch_features": ["Collect feedback and document one improvement"],
            },
            "portfolio_output": {
                "github": "Public repository with setup instructions and limitations.",
                "demo": "Short walkthrough of the project and learning outcomes.",
                "documentation": "Architecture notes, usage examples, and reflections.",
            },
            "safety_note": ROADMAP_SAFETY_NOTE,
        }

    @staticmethod
    def _personalize_prerequisites(
        roadmap: dict[str, Any], missing_skills: list[str] | None
    ) -> None:
        """Add top missing skills without altering the cached roadmap."""
        priorities = normalize_list(missing_skills)[:5]
        existing = normalize_list(roadmap.get("prerequisites"))
        roadmap["prerequisites"] = normalize_list([*priorities, *existing])

    def get_roadmap(
        self,
        career_id: str,
        career_title: str | None = None,
        missing_skills: list[str] | None = None,
    ) -> dict[str, object]:
        """Return a personalized, schema-validated roadmap."""
        normalized_id = career_id.strip()
        if not normalized_id:
            raise ValueError("career_id must not be blank")
        stored = self.load_roadmaps().get(normalized_id)
        if stored is None:
            payload = self._build_fallback(
                normalized_id,
                career_title or normalized_id.replace("_", " ").title(),
                missing_skills,
            )
        else:
            payload = deepcopy(stored)
            self._personalize_prerequisites(payload, missing_skills)
        return RoadmapResult.model_validate(payload).model_dump()
