"""Unit tests for documentation compliance and consistency."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_check_documentation_files_exist():
    """Verify that all mandatory documentation files exist."""
    files = [
        ROOT / "README.md",
        ROOT / "docs" / "architecture.md",
        ROOT / "docs" / "demo_script.md",
        ROOT / "docs" / "writeup.md",
        ROOT / "docs" / "submission_checklist.md",
    ]
    for f in files:
        assert f.exists(), f"File {f.name} does not exist"

def test_check_documentation_consistency_script():
    """Verify that the documentation consistency check script runs and passes."""
    import subprocess
    import sys

    script_path = ROOT / "scripts" / "check_documentation_consistency.py"
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    assert res.returncode == 0, f"Consistency script failed:\n{res.stdout}\n{res.stderr}"

def test_readme_specific_requirements():
    """Verify README content contains the required safety notice and commands."""
    readme_path = ROOT / "README.md"
    assert readme_path.exists()
    content = readme_path.read_text(encoding="utf-8")

    # Safety notice
    safety_notice = "This system provides educational career guidance only. It does not guarantee employment outcomes or replace professional counseling."
    assert safety_notice.lower() in content.lower(), "Missing safety notice in README"

    # Setup command
    assert "pip install -r requirements.txt" in content, "Missing setup command in README"

    # Evaluation command
    assert "python -m app.evals.evaluate_agent" in content, "Missing evaluation command in README"
