"""Verification inventory tests for Non-Functional Requirements (NFR)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_nfr_cases_exist_and_are_valid() -> None:
    """Verify nfr_cases.json structure and checks constraints."""
    nfr_file = ROOT / "app" / "evals" / "fr_nfr" / "nfr_cases.json"
    assert nfr_file.is_file(), "nfr_cases.json is missing"
    
    cases = json.loads(nfr_file.read_text(encoding="utf-8"))
    assert len(cases) >= 750, f"Expected >= 750 cases, found {len(cases)}"

    case_ids = set()
    req_counts: dict[str, int] = {}
    
    for case in cases:
        required_fields = (
            "case_id", "requirement_id", "requirement_type",
            "title", "description", "category", "priority", "expected"
        )
        for field in required_fields:
            assert field in case, f"Missing required field {field} in case {case.get('case_id')}"
            
        case_id = case["case_id"]
        assert case_id not in case_ids, f"Duplicate case ID: {case_id}"
        case_ids.add(case_id)
        
        req_id = case["requirement_id"]
        assert case["requirement_type"] == "NFR"
        
        req_counts[req_id] = req_counts.get(req_id, 0) + 1
        
        # Verify no credentials
        input_str = json.dumps(case["input_data"])
        assert "sk-" not in input_str
        assert "AIza" not in input_str
        
    for req, count in req_counts.items():
        assert count >= 50, f"Requirement {req} has {count} cases, required >= 50"
