"""Deterministic offline evaluation runner for the CareerVerse agent workflow."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from app.agents import CareerAdvisorAgent
from app.evals.evaluation_schema import (
    EvaluationCase,
    EvaluationResult,
    EvaluationSummary,
)
from app.schemas import AgentRecommendationResponse, UserProfileRequest
from app.tools.safety_tools import get_safety_notice, validate_profile_safety

CASES_PATH = Path(__file__).with_name("test_cases.json")
REQUIRED_RESPONSE_FIELDS = {
    "user_summary",
    "top_recommendations",
    "skill_gap",
    "personalized_roadmap",
    "safety_notice",
    "course_concepts_demonstrated",
}


def load_cases(path: Path = CASES_PATH) -> list[EvaluationCase]:
    """Load and validate all local evaluation cases."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Evaluation cases must use a JSON array root.")
    cases = [EvaluationCase.model_validate(item) for item in data]
    case_ids = [case.id for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Evaluation case ids must be unique.")
    return cases
