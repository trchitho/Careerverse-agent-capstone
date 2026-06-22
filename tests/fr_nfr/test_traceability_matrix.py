"""Traceability matrix compliance tests."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_traceability_matrix_completeness() -> None:
    """Verify fr_nfr_traceability_matrix.md contains no TODO or UNMAPPED entries."""
    matrix_file = ROOT / "docs" / "requirements" / "fr_nfr_traceability_matrix.md"
    assert matrix_file.is_file(), "fr_nfr_traceability_matrix.md is missing"
    
    content = matrix_file.read_text(encoding="utf-8")
    
    assert "TODO" not in content, "Traceability matrix contains unfinished TODO placeholders"
    assert "UNMAPPED" not in content, "Traceability matrix contains unmapped requirements"
    
    # Assert specific requirement IDs are present
    for req_idx in range(1, 21):
        assert f"FR-{req_idx:02d}" in content, f"Missing FR-{req_idx:02d} entry"
        
    for nfr_idx in range(1, 16):
        assert f"NFR-{nfr_idx:02d}" in content, f"Missing NFR-{nfr_idx:02d} entry"
