"""Unit tests for documentation compliance and consistency."""

from __future__ import annotations

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
        ROOT / "docs" / "runtime.md",
        ROOT / "docs" / "api_versioning.md",
        ROOT / "docs" / "api_examples.md",
        ROOT / "docs" / "persistence_plan.md",
        ROOT / "docs" / "explanation_service.md",
        ROOT / "docs" / "session_storage.md",
        ROOT / "docs" / "frontend.md",
        ROOT / "docs" / "observability.md",
        ROOT / "docs" / "feedback_analytics.md",
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
    safety_notice = (
        "This system provides educational career guidance only. It does not "
        "guarantee employment outcomes or replace professional counseling."
    )
    assert safety_notice.lower() in content.lower(), "Missing safety notice in README"

    # Setup command
    assert "pip install -r requirements.txt" in content, "Missing setup command in README"

    # Evaluation command
    assert "python -m app.evals.evaluate_agent" in content, "Missing evaluation command in README"


def test_api_versioning_documentation_requirements():
    """Verify documentation assertions regarding API versioning and compatibility constraints."""
    readme_path = ROOT / "README.md"
    api_examples_path = ROOT / "docs" / "api_examples.md"
    writeup_path = ROOT / "docs" / "writeup.md"
    arch_path = ROOT / "docs" / "architecture.md"
    api_versioning_path = ROOT / "docs" / "api_versioning.md"

    readme_content = readme_path.read_text(encoding="utf-8")
    api_examples_content = api_examples_path.read_text(encoding="utf-8")

    assert "API Versioning".lower() in readme_content.lower()
    assert "/api/v1/recommend" in readme_content
    assert "/api/v1" in api_examples_content

    # Combine docs to verify negative assertions
    # (no claim that legacy endpoints are removed / full auth)
    all_docs = (
        readme_content + "\n" +
        api_examples_content + "\n" +
        writeup_path.read_text(encoding="utf-8") + "\n" +
        arch_path.read_text(encoding="utf-8") + "\n" +
        api_versioning_path.read_text(encoding="utf-8")
    )

    import re
    assert not re.search(r"legacy endpoints? (have been )?removed", all_docs, re.IGNORECASE), \
        "Documentation incorrectly claims legacy endpoints are removed"
    assert not re.search(r"full production auth", all_docs, re.IGNORECASE), \
        "Documentation incorrectly claims full production auth"

