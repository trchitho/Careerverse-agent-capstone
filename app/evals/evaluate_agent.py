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
    searchable = _recommendation_text(response)
    if case.expected.expected_keywords and not any(
        keyword.casefold() in searchable for keyword in case.expected.expected_keywords
    ):
        failures.append("no expected career keyword appeared")

    missing = {
        skill.casefold()
        for skill in (
            response["skill_gap"]["missing_skills"]
            + response["skill_gap"]["priority_skills"]
        )
    }
    expected_missing = {
        skill.casefold() for skill in case.expected.expected_missing_skills_any
    }
    if expected_missing and missing.isdisjoint(expected_missing):
        failures.append("expected missing-skill signal was absent")

    return EvaluationResult(
        case_id=case.id,
        case_type=case.type,
        passed=not failures,
        message="response contract and expected signals valid"
        if not failures
        else "; ".join(failures),
    )


def _evaluate_security(case: EvaluationCase) -> EvaluationResult:
    """Evaluate one unsafe profile without invoking the advisor agent."""
    safety = validate_profile_safety(case.input_profile)
    serialized = json.dumps(
        {"message": safety["safe_message"], "issues": safety["issues"]},
        ensure_ascii=False,
    ).casefold()
    echoed = [
        text for text in case.expected.must_not_echo if text.casefold() in serialized
    ]
    passed = (
        not safety["is_safe"]
        and safety["risk_level"] == case.expected.expected_risk
        and not echoed
    )
    return EvaluationResult(
        case_id=case.id,
        case_type=case.type,
        passed=passed,
        message="unsafe profile blocked without echo"
        if passed
        else "security expectation failed",
    )


def _evaluate_invalid(case: EvaluationCase) -> EvaluationResult:
    """Confirm invalid input is rejected by the public request schema."""
    try:
        UserProfileRequest.model_validate(case.input_profile)
    except ValidationError:
        passed = True
    else:
        passed = False
    return EvaluationResult(
        case_id=case.id,
        case_type=case.type,
        passed=passed,
        message="invalid profile rejected" if passed else "invalid profile was accepted",
    )


def evaluate_case(
    case: EvaluationCase,
    agent: CareerAdvisorAgent | None = None,
) -> EvaluationResult:
    """Dispatch one validated case to its deterministic evaluator."""
    advisor = agent or CareerAdvisorAgent()
    try:
        if case.expected.status == "success":
            return _evaluate_success(case, advisor)
        if case.expected.status == "blocked":
            return _evaluate_security(case)
        return _evaluate_invalid(case)
    except (KeyError, TypeError, ValueError, ValidationError) as error:
        return EvaluationResult(
            case_id=case.id,
            case_type=case.type,
            passed=False,
            message=f"{type(error).__name__}: {error}",
        )


def run_evaluation(cases: list[EvaluationCase] | None = None) -> tuple[
    list[EvaluationResult], EvaluationSummary
]:
    """Run all cases and return deterministic results with aggregate score."""
    selected = cases or load_cases()
    agent = CareerAdvisorAgent()
    results = [evaluate_case(case, agent) for case in selected]
    passed = sum(result.passed for result in results)
    failed = len(results) - passed
    score = round((passed / len(results) * 100) if results else 0.0, 2)
    summary = EvaluationSummary(
        total=len(results),
        passed=passed,
        failed=failed,
        skipped=0,
        score=score,
    )
    return results, summary


def main() -> int:
    """Run the local evaluator, print results, and return its process status."""
    results, summary = run_evaluation()
    for result in results:
        label = "PASS" if result.passed else "FAIL"
        print(f"[{label}] {result.case_id} — {result.message}")
    print("\nEvaluation Summary")
    print(f"Total: {summary.total}")
    print(f"Passed: {summary.passed}")
    print(f"Failed: {summary.failed}")
    print(f"Skipped: {summary.skipped}")
    print(f"Score: {summary.score:.2f}%")
    return 0 if summary.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
