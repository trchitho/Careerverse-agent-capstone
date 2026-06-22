"""Runner verification checks for Non-Functional Requirements."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_reports_are_generated() -> None:
    """Verify that verify-report JSON and MD files are created correctly in docs/audits."""
    json_report = ROOT / "docs" / "audits" / "fr_nfr_verification_report.json"
    md_report = ROOT / "docs" / "audits" / "fr_nfr_verification_report.md"
    
    assert json_report.is_file(), "Verification report JSON is missing"
    assert md_report.is_file(), "Verification report Markdown is missing"
