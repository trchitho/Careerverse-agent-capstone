"""Unit tests asserting correctness and properties of GitHub Actions workflow files."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"


def test_ci_workflow_properties() -> None:
    """Verify properties of ci.yml workflow."""
    ci_file = WORKFLOW_DIR / "ci.yml"
    assert ci_file.is_file(), "ci.yml is missing"

    content = ci_file.read_text(encoding="utf-8")

    # Assert standard requirements
    assert "runs-on: ubuntu-latest" in content
    assert "python-version: \"3.11\"" in content or "python-version: '3.11'" in content
    assert "validate_domain_dataset.py" in content
    assert "audit_prompt_0_to_7.py" in content
    assert "smoke_test_api.py" in content
    assert "evaluate_agent" in content
    assert "check_documentation_consistency.py" in content
    assert "compileall" in content
    assert "ruff check" in content
    assert "pytest" in content

    # Assert frontend build is called if frontend exists
    assert "npm run build" in content


def test_security_workflow_properties() -> None:
    """Verify properties of security.yml workflow."""
    sec_file = WORKFLOW_DIR / "security.yml"
    assert sec_file.is_file(), "security.yml is missing"

    content = sec_file.read_text(encoding="utf-8")

    assert "Verify no .env files are tracked" in content
    assert "Verify no cache or build artifacts are tracked" in content
    assert "Scan for obvious hardcoded credentials" in content
    assert "test_security_hygiene.py" in content
    assert "test_safety.py" in content

    # Assert no secrets or paid vendors are requested
    assert "secrets." not in content
    assert "sonar" not in content.lower()
    assert "snyk" not in content.lower()
