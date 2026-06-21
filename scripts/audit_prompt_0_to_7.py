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


REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    ".env.example",
    ".gitignore",
    "requirements.txt",
    "pyproject.toml",
    "app/main.py",
    "app/core/config.py",
    "app/core/constants.py",
    "app/data/careers.json",
    "app/data/skills.json",
    "app/data/roadmaps.json",
    "app/schemas/profile_schema.py",
    "app/schemas/domain_schema.py",
    "app/tools/career_tools.py",
    "app/agents/career_advisor_agent.py",
    "app/agents/skill_gap_agent.py",
    "app/agents/roadmap_agent.py",
    "app/mcp_server/career_mcp_server.py",
    "app/skills/career_advisor/SKILL.md",
    "app/skills/code_quality/SKILL.md",
    "app/skills/security_review/SKILL.md",
    "app/skills/kaggle_submission/SKILL.md",
]

SKILL_MARKERS = [
    "# Career Advisor Skill",
    "Purpose",
    "When to Use",
    "When Not to Use",
    "Required Inputs",
    "Optional Inputs",
    "Input Validation Rules",
    "Workflow Overview",
    "Detailed Workflow",
    "Tool Usage",
    "Output Contract",
    "Safety and Responsible AI Rules",
    "Failure Handling",
    "Quality Checklist",
    "Example Input",
    "Example Output",
    "Testing and Evaluation Notes",
    "Implementation Boundaries",
    "Future Extensions",
    "UserProfileRequest",
    "AgentRecommendationResponse",
    "CareerAdvisorAgent",
    "SkillGapAgent",
    "RoadmapAgent",
    "MCP-style",
    "does not guarantee employment outcomes",
]
