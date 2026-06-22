"""Verification inventory tests for Functional Requirements (FR)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_fr_cases_exist_and_are_valid() -> None:
    """Verify fr_cases.json structure and checks constraints."""
    fr_file = ROOT / "app" / "evals" / "fr_nfr" / "fr_cases.json"
    assert fr_file.is_file(), "fr_cases.json is missing"
    
    cases = json.loads(fr_file.read_text(encoding="utf-8"))
    assert len(cases) >= 1000, f"Expected >= 1000 cases, found {len(cases)}"

    case_ids = set()
    req_counts: dict[str, int] = {}
    
    for case in cases:
        # Check required fields
        for field in ("case_id", "requirement_id", "requirement_type", "title", "description", "category", "priority", "expected"):
            assert field in case, f"Missing required field {field} in case {case.get('case_id')}"
            
        case_id = case["case_id"]
        assert case_id not in case_ids, f"Duplicate case ID: {case_id}"
        case_ids.add(case_id)
        
        req_id = case["requirement_id"]
        assert case["requirement_type"] == "FR"
        
        req_counts[req_id] = req_counts.get(req_id, 0) + 1
        
        # Verify no credentials
        input_str = json.dumps(case["input_data"])
        assert "sk-" not in input_str
        assert "AIza" not in input_str
        
    for req, count in req_counts.items():
        assert count >= 50, f"Requirement {req} has {count} cases, required >= 50"
