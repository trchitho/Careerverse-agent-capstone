"""Contract tests for the deterministic local evaluation pipeline."""

import json
import os
import subprocess
import sys
from pathlib import Path

from app.evals.evaluate_agent import load_cases, run_evaluation

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "app" / "evals" / "test_cases.json"


def raw_cases() -> list[dict[str, object]]:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))


def test_evaluation_dataset_has_required_coverage() -> None:
    cases = raw_cases()
    case_types = {case["type"] for case in cases}

    assert len(cases) >= 10
    assert {"normal", "edge", "security", "invalid"} <= case_types


def test_evaluation_case_ids_are_unique() -> None:
    case_ids = [case["id"] for case in raw_cases()]

    assert len(case_ids) == len(set(case_ids))


def test_evaluation_cases_validate_with_schema() -> None:
    cases = load_cases()

    assert len(cases) == len(raw_cases())
    assert all(case.input_profile and case.expected.status for case in cases)


def test_in_process_evaluation_passes_all_cases() -> None:
    results, summary = run_evaluation()

    assert summary.total >= 10
    assert summary.passed == summary.total
    assert summary.failed == 0
    assert summary.score == 100.0
    assert all(result.passed for result in results)


def test_evaluation_includes_security_and_invalid_results() -> None:
    results, _ = run_evaluation()
    result_types = {result.case_type for result in results}

    assert "security" in result_types
    assert "invalid" in result_types
