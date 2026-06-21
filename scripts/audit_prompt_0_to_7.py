"""Offline compliance audit for CareerVerse Agent prompts 0 through 7."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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


def load_json(relative_path: str) -> Any:
    """Load one UTF-8 JSON document from the repository."""
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def audit_files() -> None:
    """Verify files required by prompts 0 through 7."""
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    record("required files", not missing, ", ".join(missing))

    agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    agents_markers = [
        "10–30 lines",
        "Never commit",
        "python -m compileall app",
        "Implemented features and future work",
    ]
    absent = [marker for marker in agents_markers if marker not in agents_text]
    record("AGENTS.md project rules", not absent, ", ".join(absent))

    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    missing_markers = [marker for marker in SKILL_MARKERS if marker not in skill_text]
    record("career advisor skill contract", not missing_markers, ", ".join(missing_markers))


def audit_dataset() -> None:
    """Verify dataset scale, uniqueness, and roadmap mapping."""
    careers = load_json("app/data/careers.json")
    skills = load_json("app/data/skills.json")
    roadmaps = load_json("app/data/roadmaps.json")

    record("career count", isinstance(careers, list) and len(careers) >= 80, str(len(careers)))
    record("skill count", isinstance(skills, list) and len(skills) >= 250, str(len(skills)))
    record(
        "roadmap count",
        isinstance(roadmaps, dict) and len(roadmaps) == len(careers),
        str(len(roadmaps)),
    )

    career_ids = [career.get("id") for career in careers]
    career_titles = [career.get("title") for career in careers]
    skill_ids = [skill.get("id") for skill in skills]
    skill_names = [skill.get("name") for skill in skills]
    record("unique career ids", len(career_ids) == len(set(career_ids)))
    record("unique career titles", len(career_titles) == len(set(career_titles)))
    record("unique skill ids", len(skill_ids) == len(set(skill_ids)))
    record("unique skill names", len(skill_names) == len(set(skill_names)))

    roadmap_ids = set(roadmaps)
    career_id_set = set(career_ids)
    record("career roadmap mapping", roadmap_ids == career_id_set)

    career_fields = {
        "id",
        "title",
        "description",
        "required_skills",
        "recommended_for",
        "market_relevance",
        "safety_note",
    }
    skill_fields = {"id", "name", "category", "level", "description"}
    roadmap_fields = {
        "career_id",
        "career_title",
        "thirty_day_plan",
        "eight_week_plan",
        "recommended_mini_project",
        "portfolio_output",
        "safety_note",
    }
    record("career required fields", all(career_fields <= career.keys() for career in careers))
    record("skill required fields", all(skill_fields <= skill.keys() for skill in skills))
    valid_roadmaps = all(roadmap_fields <= item.keys() for item in roadmaps.values())
    record("roadmap required fields", valid_roadmaps)

    serialized_data = json.dumps([careers, skills, roadmaps], ensure_ascii=False).lower()
    unsafe_claims = [
        "guaranteed employment",
        "guaranteed job",
        "guaranteed salary",
        "100% accurate",
    ]
    found_claims = [claim for claim in unsafe_claims if claim in serialized_data]
    record("dataset responsible claims", not found_claims, ", ".join(found_claims))


def demo_payload() -> dict[str, object]:
    """Return the synthetic profile used by audit smoke checks."""
    return {
        "name": "Demo User",
        "education": "Final-year IT student",
        "interests": ["AI", "web development", "product building"],
        "skills": ["Python", "React", "SQL"],
        "career_goal": "Become an AI full-stack developer",
        "preferred_learning_style": "project_based",
        "language": "en",
        "experience_level": "university",
        "time_budget_hours_per_week": 8,
    }


def audit_imports_and_tools() -> None:
    """Exercise core schemas, scoring, agents, and MCP tools."""
    from app.agents.career_advisor_agent import CareerAdvisorAgent
    from app.agents.roadmap_agent import RoadmapAgent
    from app.agents.skill_gap_agent import SkillGapAgent
    from app.mcp_server.career_mcp_server import list_available_careers
    from app.schemas.profile_schema import AgentRecommendationResponse, UserProfileRequest
    from app.tools.career_tools import recommend_careers

    profile = UserProfileRequest.model_validate(demo_payload())
    recommendations = recommend_careers(profile, top_k=3)
    response = CareerAdvisorAgent().run(profile)
    AgentRecommendationResponse.model_validate(response)

    skill_gap = SkillGapAgent().analyze(["Python"], ["Python", "FastAPI"])
    roadmap = RoadmapAgent().get_roadmap(recommendations[0]["career_id"])
    catalog = list_available_careers(limit=5)

    record("core imports", True)
    record("deterministic recommendations", recommendations == recommend_careers(profile, top_k=3))
    record("recommendation top_k", len(recommendations) == 3)
    record(
        "recommendation contract",
        all(
            key in recommendations[0]
            for key in (
                "score_breakdown",
                "matched_reasons",
                "matched_skills",
                "missing_skills_preview",
                "safety_note",
            )
        ),
    )
    record("skill gap agent", 0 <= skill_gap["readiness_score"] <= 100)
    record("roadmap agent", len(roadmap["thirty_day_plan"]) == 4)
    record("MCP career listing", catalog["count"] == 5)


def audit_api() -> None:
    """Smoke test all critical public endpoints."""
    from app.main import app

    client = TestClient(app)
    requests = [
        ("GET /", client.get("/")),
        ("GET /metadata", client.get("/metadata")),
        ("POST /profiles/validate", client.post("/profiles/validate", json=demo_payload())),
        ("POST /recommend", client.post("/recommend", json=demo_payload())),
        ("GET /tools", client.get("/tools")),
        ("GET /mcp/careers", client.get("/mcp/careers?limit=5")),
        ("GET /mcp/skills", client.get("/mcp/skills?limit=5")),
        ("GET /mcp/search/careers", client.get("/mcp/search/careers?q=AI")),
        ("GET /mcp/search/skills", client.get("/mcp/search/skills?q=Python")),
    ]
    for name, response in requests:
        record(name, response.status_code == 200, str(response.status_code))

    record(
        "controlled API validation",
        client.post("/recommend", json={}).status_code == 422
        and client.get("/mcp/careers/not_real_id").status_code == 404,
    )


def tracked_files() -> list[str]:
    """Return repository paths tracked by Git."""
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def audit_hygiene() -> None:
    """Check tracked secrets, caches, local environments, and build output."""
    tracked = tracked_files()
    artifact_pattern = re.compile(
        r"(^|/)(\.env$|__pycache__|\.pytest_cache|\.ruff_cache|node_modules|dist|build)(/|$)"
        r"|\.pyc$"
    )
    artifacts = [path for path in tracked if artifact_pattern.search(path.replace("\\", "/"))]
    record("tracked artifact hygiene", not artifacts, ", ".join(artifacts))

    secret_pattern = re.compile(
        r"(GOOGLE_API_KEY=AIza|sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]+|"
        r"github_pat_[A-Za-z0-9_]+|password\s*=\s*\S+|token\s*=\s*\S+|"
        r"secret\s*=\s*\S+|BEGIN PRIVATE KEY)",
        re.IGNORECASE,
    )
    risky_files: list[str] = []
    text_suffixes = {".py", ".json", ".toml", ".txt", ".env", ""}
    for path in tracked:
        candidate = ROOT / path
        excluded = {
            ".env.example",
            "app/tools/safety_tools.py",
            "scripts/audit_prompt_0_to_7.py",
            "tests/test_safety.py",
            "tests/test_safety_tools.py",
            "tests/test_security_hygiene.py",
        }
        if candidate.suffix.lower() not in text_suffixes or path in excluded:
            continue
        try:
            content = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if secret_pattern.search(content):
            risky_files.append(path)
    record("tracked secret hygiene", not risky_files, ", ".join(risky_files))

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_markers = [
        "# CareerVerse Agent",
        "## Track",
        "## Problem",
        "## Solution",
        "## Setup",
        "## API",
        "## Domain Data",
        "## Input Validation",
        "## Career Scoring Engine",
        "## Multi-Agent Workflow",
        "## MCP-Style Tool Server",
        "## Agent Skills",
        "## Security",
        "## Development",
    ]
    missing = [marker for marker in readme_markers if marker not in readme]
    record("README coverage", not missing, ", ".join(missing))


def main() -> int:
    """Run all compliance audit sections and return a process exit code."""
    sections = [
        ("files and rules", audit_files),
        ("domain dataset", audit_dataset),
        ("imports and tools", audit_imports_and_tools),
        ("API compatibility", audit_api),
        ("security and Git hygiene", audit_hygiene),
    ]
    for title, audit in sections:
        print(f"\n=== {title.upper()} ===")
        try:
            audit()
        except (ImportError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
            record(title, False, str(error))

    passed = sum(result for _, result in checks)
    print(f"\nChecks passed: {passed}/{len(checks)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Errors: {len(errors)}")
    verdict = "PASS" if not errors and not warnings else "PASS_WITH_MINOR_NOTES"
    if errors:
        verdict = "FAIL"
    print(f"FINAL VERDICT: {verdict}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
