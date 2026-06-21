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


def _recommendation_text(response: dict[str, object]) -> str:
    """Build searchable recommendation text for non-brittle keyword checks."""
    recommendations = response["top_recommendations"]
    parts: list[str] = []
    for item in recommendations:
        parts.extend(
            [
                str(item["title"]),
                str(item["description"]),
                " ".join(item["matched_reasons"]),
            ]
        )
    return " ".join(parts).casefold()


def _validate_response_contract(response: dict[str, object], top_k: int) -> list[str]:
    """Return contract failures for a successful workflow response."""
    failures: list[str] = []
    if not REQUIRED_RESPONSE_FIELDS.issubset(response):
        failures.append("required response fields are missing")
    validated = AgentRecommendationResponse.model_validate(response)
    if len(validated.top_recommendations) != top_k:
        failures.append(f"expected {top_k} recommendations")
    if any(not 0 <= item.score <= 100 for item in validated.top_recommendations):
        failures.append("recommendation score outside 0-100")
    if not 0 <= validated.skill_gap.readiness_score <= 100:
        failures.append("readiness score outside 0-100")
    if len(validated.personalized_roadmap.thirty_day_plan) != 4:
        failures.append("30-day roadmap does not contain four weeks")
    if len(validated.personalized_roadmap.eight_week_plan) != 8:
        failures.append("8-week roadmap does not contain eight weeks")
    if validated.safety_notice != get_safety_notice():
        failures.append("canonical safety notice is missing")
    return failures


def _evaluate_success(case: EvaluationCase, agent: CareerAdvisorAgent) -> EvaluationResult:
    """Evaluate one normal or edge workflow case."""
    profile = UserProfileRequest.model_validate(case.input_profile)
    safety = validate_profile_safety(profile)
    if not safety["is_safe"]:
        return EvaluationResult(
            case_id=case.id,
            case_type=case.type,
            passed=False,
            message="safe profile was blocked",
        )
    response = agent.run(safety["redacted_profile"], top_k=case.expected.top_k)
    failures = _validate_response_contract(response, case.expected.top_k)
