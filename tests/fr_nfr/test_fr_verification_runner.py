"""Runner verification checks for Functional Requirements."""

from __future__ import annotations

from pathlib import Path
from app.evals.fr_nfr.fr_nfr_schema import RequirementCase
from app.evals.fr_nfr.run_fr_nfr_verification import run_checks

ROOT = Path(__file__).resolve().parents[2]


def test_runner_imports_and_validates_schema() -> None:
    """Verify that runner can load and parse schema structures."""
    sample_case = {
        "case_id": "FR-01-TC-999",
        "requirement_id": "FR-01",
        "requirement_type": "FR",
        "title": "Test case",
        "description": "desc",
        "category": "positive",
        "priority": "P0",
        "preconditions": [],
        "input_data": {},
        "steps": [],
        "expected": "ok",
        "negative": False,
        "automation_level": "automated",
        "verification_method": "file_scan",
        "target_files": [],
        "target_endpoints": [],
        "tags": []
    }
    parsed = RequirementCase(**sample_case)
    assert parsed.case_id == "FR-01-TC-999"


def test_runner_run_succeeds() -> None:
    """Verify that run_checks() executes successfully and returns exit code 0."""
    exit_code = run_checks()
    assert exit_code == 0
