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


def test_cache_and_build_artifacts_are_not_tracked() -> None:
    forbidden = (
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        "node_modules",
        "/dist/",
        "/build/",
    )
    tracked = [path.replace("\\", "/") for path in git_files()]

    assert not any(path.endswith(".pyc") for path in tracked)
    assert not any(marker in f"/{path}/" for path in tracked for marker in forbidden)


def test_tracked_files_do_not_contain_obvious_credentials() -> None:
    credential_markers = (
        "s" + "k-",
        "AI" + "za",
        "gh" + "p_",
        "github_" + "pat_",
        "BEGIN " + "PRIVATE KEY",
    )
    excluded = {"tests/test_security_hygiene.py", "scripts/audit_prompt_0_to_7.py"}
    findings: list[str] = []
    for relative_path in git_files():
        if relative_path in excluded or relative_path == ".env.example":
            continue
        path = ROOT / relative_path
        if path.suffix.lower() not in {".py", ".json", ".md", ".toml", ".txt"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(marker in content for marker in credential_markers):
            findings.append(relative_path)

    assert findings == []


def test_recommendation_contains_canonical_notice() -> None:
    payload = {
        "name": "Demo",
        "education": "IT student",
        "interests": ["AI"],
        "skills": ["Python"],
        "career_goal": "Build AI products",
    }
    response = TestClient(app).post("/recommend", json=payload)

    assert response.status_code == 200
    assert response.json()["safety_notice"] == get_safety_notice()
