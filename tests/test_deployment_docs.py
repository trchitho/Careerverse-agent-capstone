"""Unit tests asserting deployment configurations and operations runbooks constraints."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
SCRIPTS_DIR = ROOT / "scripts"


def test_deployment_guide_checks() -> None:
    """Verify deployment guide contents and compliance."""
    guide = DOCS_DIR / "deployment.md"
    assert guide.is_file(), "deployment.md is missing"

    content = guide.read_text(encoding="utf-8")

    assert "Google Cloud Run" in content
    assert "docker build" in content
    assert "docker run" in content
    assert "gcloud run deploy" in content

    # Assert no live claims or secret exposures
    assert "is deployed at" not in content.lower()
    assert "is live at" not in content.lower()
    assert "AIzaSy" not in content


def test_operations_runbook_checks() -> None:
    """Verify operations runbook contents and compliance."""
    runbook = DOCS_DIR / "operations_runbook.md"
    assert runbook.is_file(), "operations_runbook.md is missing"

    content = runbook.read_text(encoding="utf-8")

    assert "/api/v1/health/live" in content
    assert "/api/v1/health/ready" in content
    assert "Rollback" in content
    assert "never copy" in content.lower() or "never paste" in content.lower()


def test_pre_deploy_check_script_properties() -> None:
    """Verify pre-deploy check script constraints."""
    script = SCRIPTS_DIR / "pre_deploy_check.py"
    assert script.is_file(), "pre_deploy_check.py is missing"

    content = script.read_text(encoding="utf-8")

    # Verify standard validation gates are invoked
    assert "validate_domain_dataset.py" in content
    assert "smoke_test_api.py" in content
    assert "evaluate_agent" in content
    assert "check_documentation_consistency.py" in content
    assert "compileall" in content
    assert "ruff" in content
    assert "pytest" in content

    # Verify no deployment actions occur
    assert not re.search(r"gcloud\s+run\s+deploy", content), \
        "Pre-deployment check script should not trigger real deployment."
