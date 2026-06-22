"""Full project documentation and claims regression tests."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_docs_existence() -> None:
    required_paths = [
        ROOT / "docs" / "requirements" / "fr_catalog.md",
        ROOT / "docs" / "requirements" / "nfr_catalog.md",
        ROOT / "docs" / "requirements" / "fr_nfr_traceability_matrix.md",
        ROOT / "docs" / "requirements" / "test_strategy.md",
        ROOT / "docs" / "requirements" / "test_case_design.md",
        ROOT / "docs" / "deployment.md",
        ROOT / "docs" / "operations_runbook.md",
        ROOT / "docs" / "launch" / "market_launch_checklist.md",
        ROOT / "docs" / "launch" / "product_one_pager.md",
        ROOT / "docs" / "launch" / "user_onboarding.md",
        ROOT / "docs" / "launch" / "faq.md",
        ROOT / "docs" / "launch" / "known_limitations.md",
        ROOT / "docs" / "launch" / "privacy_note.md",
        ROOT / "docs" / "launch" / "responsible_ai_note.md",
    ]
    for p in required_paths:
        assert p.is_file(), f"Required docs missing: {p.name}"


def test_docs_claims_safety() -> None:
    # Read writeup and launch pack to verify disclaimer assertions
    launch_docs = (ROOT / "docs" / "launch").glob("*.md")
    combined = ""
    for d in launch_docs:
        combined += d.read_text(encoding="utf-8") + "\n"
        
    combined += (ROOT / "README.md").read_text(encoding="utf-8") + "\n"
    combined += (ROOT / "docs" / "writeup.md").read_text(encoding="utf-8") + "\n"
    
    lowered = combined.lower()
    
    # Assert no job guarantee or clinical replacement claims
    assert "educational guidance" in lowered or "learning guidance" in lowered
    assert "no guarantee" in lowered or "does not guarantee" in lowered
    assert "counseling" in lowered
    
    # Assert that no fake deployed URLs are claimed
    assert "is live at" not in lowered
    assert "is deployed at" not in lowered
    
    # Verify no claims of PostgreSQL or auth being implemented in production
    assert not re.search(r"production database is implemented", lowered)
    assert not re.search(r"postgresql is implemented", lowered)
    assert not re.search(r"full auth is implemented", lowered)
