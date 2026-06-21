"""Repository-level security hygiene regression tests."""

import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.tools.safety_tools import get_safety_notice

ROOT = Path(__file__).resolve().parents[1]


def git_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def test_local_environment_is_not_tracked() -> None:
    assert ".env" not in git_files()
    example = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "GOOGLE_API_KEY=\n" in example.replace("\r\n", "\n")
