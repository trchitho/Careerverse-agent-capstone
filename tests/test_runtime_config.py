"""Tests for CareerVerse Agent runtime configuration."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_dockerfile_config() -> None:
    """Verify Dockerfile exists and meets production constraints."""
    dockerfile_path = ROOT / "Dockerfile"
    assert dockerfile_path.exists(), "Dockerfile must exist at repository root"

    content = dockerfile_path.read_text(encoding="utf-8")
    assert "python:3.11" in content or "python:3.12" in content or "FROM python:" in content, "Dockerfile must use Python 3.11+"
    assert "uvicorn" in content, "Dockerfile must contain uvicorn"
    assert "app.main:app" in content, "Dockerfile must reference app.main:app"
    assert "EXPOSE 8000" in content, "Dockerfile must expose port 8000"
    assert "api_key" not in content.lower(), "Dockerfile must not contain real API keys"
