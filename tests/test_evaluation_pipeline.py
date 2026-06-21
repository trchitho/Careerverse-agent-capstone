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
