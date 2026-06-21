"""Offline compliance audit for CareerVerse Agent prompts 0 through 7."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "app" / "data"
SKILL_PATH = ROOT / "app" / "skills" / "career_advisor" / "SKILL.md"

errors: list[str] = []
warnings: list[str] = []
checks: list[tuple[str, bool]] = []


def record(name: str, passed: bool, detail: str = "") -> None:
    """Record and print one audit check."""
    checks.append((name, passed))
    suffix = f" - {detail}" if detail else ""
    print(f"{'PASS' if passed else 'FAIL'}: {name}{suffix}")
    if not passed:
        errors.append(f"{name}{suffix}")
