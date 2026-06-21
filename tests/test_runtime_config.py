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


def test_dockerignore_config() -> None:
    """Verify .dockerignore exists and excludes secrets and caches."""
    dockerignore_path = ROOT / ".dockerignore"
    assert dockerignore_path.exists(), ".dockerignore must exist at repository root"

    content = dockerignore_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]

    assert ".env" in lines or ".env*" in lines, ".dockerignore must exclude .env"
    assert "__pycache__/" in lines or "__pycache__" in lines, ".dockerignore must exclude pycache"
    assert ".pytest_cache/" in lines or ".pytest_cache" in lines, ".dockerignore must exclude pytest cache"
    assert "app/data" not in lines and "app/data/" not in lines, ".dockerignore must not exclude app/data"


def test_docker_compose_config() -> None:
    """Verify docker-compose.yml exists and contains required structures."""
    compose_path = ROOT / "docker-compose.yml"
    assert compose_path.exists(), "docker-compose.yml must exist at repository root"

    content = compose_path.read_text(encoding="utf-8")
    assert "careerverse-api" in content or "careerverse-agent-api" in content, "docker-compose must name the API service"
    assert "8000:8000" in content, "docker-compose must map port 8000"
    assert "api_key" not in content.lower(), "docker-compose must not contain real secrets"


def test_runtime_docs_and_scripts() -> None:
    """Verify docs/runtime.md and scripts/docker_smoke_check.py exist."""
    runtime_docs_path = ROOT / "docs" / "runtime.md"
    assert runtime_docs_path.exists(), "docs/runtime.md must exist"

    content = runtime_docs_path.read_text(encoding="utf-8")
    assert "Docker Runtime" in content, "docs/runtime.md must document Docker"
    assert "docker build" in content, "docs/runtime.md must contain docker build command"

    smoke_check_path = ROOT / "scripts" / "docker_smoke_check.py"
    assert smoke_check_path.exists(), "scripts/docker_smoke_check.py must exist"
