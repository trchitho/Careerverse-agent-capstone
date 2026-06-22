"""Unit tests verifying product launch pack documentation content and disclaimers."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCH_DIR = ROOT / "docs" / "launch"


def test_launch_pack_files_exist() -> None:
    """Verify that all mandatory product launch materials exist."""
    files = [
        LAUNCH_DIR / "market_launch_checklist.md",
        LAUNCH_DIR / "product_one_pager.md",
        LAUNCH_DIR / "user_onboarding.md",
        LAUNCH_DIR / "faq.md",
        LAUNCH_DIR / "known_limitations.md",
        LAUNCH_DIR / "privacy_note.md",
        LAUNCH_DIR / "responsible_ai_note.md",
    ]
    for f in files:
        assert f.is_file(), f"Launch doc missing: {f.name}"


def test_launch_pack_disclaimers() -> None:
    """Verify launch pack files contain safety and responsible AI disclaimers."""
    launch_docs = LAUNCH_DIR.glob("*.md")
    
    # Combined content of all launch guides
    combined_content = ""
    for doc in launch_docs:
        combined_content += doc.read_text(encoding="utf-8") + "\n"

    lowered = combined_content.lower()

    # Verify disclaimers are stated honestly
    assert "educational guidance" in lowered or "learning guidance" in lowered
    assert "no guarantee" in lowered or "does not guarantee" in lowered
    assert "counseling" in lowered
    assert "clinical" in lowered or "psychological" in lowered

    # Verify no claims of production database or auth are made
    assert "production database" in lowered or "postgresql" in lowered or "neo4j" in lowered
    assert "in-memory" in lowered or "ephemeral" in lowered or "process ram" in lowered
    assert "no production authentication" in lowered or "does not enforce" in lowered

    # Assert no fake live links are present
    assert "is live at" not in lowered
    assert "is deployed at" not in lowered
