"""Validate the local CareerVerse domain data catalog."""

import json
import re
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
ALLOWED_CATEGORIES = {
    "frontend", "backend", "ai", "data", "cloud",
    "security", "soft-skill", "product", "testing", "devops",
}
ALLOWED_LEVELS = {"beginner", "intermediate", "advanced"}
MARKET_LEVELS = {"medium", "high", "emerging"}
CAREER_FIELDS = {
    "id", "title", "description", "target_users", "required_skills",
    "nice_to_have_skills", "recommended_for", "sample_projects",
    "market_relevance", "explanation", "safety_note",
}


def load_json(filename: str) -> Any:
    """Load a UTF-8 JSON file from the domain data directory."""
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


def validate_skills(skills: Any) -> tuple[set[str], list[str]]:
    """Validate skill records and return their unique names."""
    errors: list[str] = []
    if not isinstance(skills, list) or len(skills) < 40:
        return set(), ["skills.json must contain at least 40 skill objects"]

    names = [skill.get("name") for skill in skills if isinstance(skill, dict)]
    if len(names) != len(set(names)):
        errors.append("skills.json contains duplicate skill names")

    for index, skill in enumerate(skills):
        if not isinstance(skill, dict):
            errors.append(f"skill {index} must be an object")
            continue
        if set(skill) != {"name", "category", "level", "description"}:
            errors.append(f"skill {index} has invalid fields")
        if skill.get("category") not in ALLOWED_CATEGORIES:
            errors.append(f"skill {index} has an invalid category")
        if skill.get("level") not in ALLOWED_LEVELS:
            errors.append(f"skill {index} has an invalid level")
    return set(names), errors


def validate_careers(careers: Any, skill_names: set[str]) -> tuple[set[str], list[str]]:
    """Validate career records and references to the skill catalog."""
    errors: list[str] = []
    if not isinstance(careers, list) or len(careers) < 8:
        return set(), ["careers.json must contain at least 8 career objects"]

    ids = [career.get("id") for career in careers if isinstance(career, dict)]
    if len(ids) != len(set(ids)):
        errors.append("careers.json contains duplicate career ids")

    for index, career in enumerate(careers):
        if not isinstance(career, dict) or set(career) != CAREER_FIELDS:
            errors.append(f"career {index} has invalid fields")
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", career["id"]):
            errors.append(f"career {index} id must use snake_case")
        if career["market_relevance"].get("level") not in MARKET_LEVELS:
            errors.append(f"career {career['id']} has an invalid market level")
        referenced = set(career["required_skills"] + career["nice_to_have_skills"])
        missing = sorted(referenced - skill_names)
        if missing:
            errors.append(f"career {career['id']} references missing skills: {missing}")
    return set(ids), errors


def validate_plan(career_id: str, name: str, plan: Any, weeks: int) -> list[str]:
    """Validate week numbering, tasks, and deliverables in one plan."""
    if not isinstance(plan, list) or len(plan) != weeks:
        return [f"{career_id} {name} must contain {weeks} weeks"]

    errors: list[str] = []
    if [item.get("week") for item in plan if isinstance(item, dict)] != list(
        range(1, weeks + 1)
    ):
        errors.append(f"{career_id} {name} has invalid week numbering")
    for item in plan:
        if not isinstance(item, dict) or set(item) != {"week", "focus", "tasks", "deliverable"}:
            errors.append(f"{career_id} {name} has an invalid week record")
            continue
        if not 2 <= len(item["tasks"]) <= 5:
            errors.append(f"{career_id} {name} week {item['week']} has invalid task count")
    return errors


def validate_roadmaps(roadmaps: Any, career_ids: set[str]) -> list[str]:
    """Validate roadmap coverage and required roadmap structure."""
    if not isinstance(roadmaps, dict) or set(roadmaps) != career_ids:
        return ["roadmaps.json keys must exactly match career ids"]
    errors: list[str] = []
    required = {"career_title", "duration_options", "thirty_day_plan", "eight_week_plan",
                "recommended_mini_project", "portfolio_output"}
