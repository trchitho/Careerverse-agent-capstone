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
    record("roadmap required fields", all(roadmap_fields <= item.keys() for item in roadmaps.values()))


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
