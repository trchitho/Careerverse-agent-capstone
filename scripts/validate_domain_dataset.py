"""Validate generated CareerVerse domain datasets and cross-references."""

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "app" / "data"
FILES = ("careers.json", "skills.json", "roadmaps.json")
CAREER_FAMILIES = {
    "Software Engineering", "AI / ML / Agent", "Data", "Cloud / DevOps",
    "Security", "Product / Business", "Education / Social Good",
    "Tech Support / Operations",
}
SKILL_CATEGORIES = {
    "frontend", "backend", "ai", "data", "cloud", "security", "soft-skill",
    "product", "testing", "devops", "database", "architecture", "documentation",
}
SKILL_LEVELS = {"beginner", "intermediate", "advanced"}
CAREER_LEVELS = {"entry", "entry_to_mid", "mid", "advanced"}
MARKET_LEVELS = {"medium", "high", "emerging"}
DIFFICULTY_LEVELS = {"low", "medium", "high"}


def load_json(filename: str) -> Any:
    """Load one required UTF-8 JSON file."""
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


CAREER_FIELDS = {
    "id", "title", "family", "level", "description", "target_users",
    "required_skills", "nice_to_have_skills", "recommended_for", "avoid_if",
    "sample_projects", "daily_work", "growth_paths", "market_relevance",
    "learning_difficulty", "personality_fit", "explanation", "safety_note",
}
SKILL_FIELDS = {
    "id", "name", "category", "level", "aliases", "description",
    "used_in_roles", "related_skills", "learning_resources_keywords",
    "assessment_hint",
}
ROADMAP_FIELDS = {
    "career_title", "career_id", "duration_options", "prerequisites",
    "thirty_day_plan", "eight_week_plan", "recommended_mini_project",
    "portfolio_output", "safety_note",
}
WEEK_FIELDS = {
    "week", "focus", "learning_goals", "tasks", "deliverable",
    "skills_practiced", "checkpoint",
}


def validate_files() -> tuple[dict[str, Any], list[str]]:
    """Check required files and load valid JSON payloads."""
    payloads: dict[str, Any] = {}
    errors: list[str] = []
    for filename in FILES:
        path = DATA_DIR / filename
        if not path.is_file():
            errors.append(f"missing required file: {path}")
            continue
        try:
            payloads[filename] = load_json(filename)
        except json.JSONDecodeError as error:
            errors.append(f"{filename} is invalid JSON: {error}")
    return payloads, errors


def duplicate_values(values: list[str]) -> set[str]:
    """Return values occurring more than once."""
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def validate_skills(skills: Any) -> tuple[set[str], list[str]]:
    """Validate skill records and return known names."""
    errors: list[str] = []
    if not isinstance(skills, list) or len(skills) < 250:
        return set(), ["skills.json must contain at least 250 records"]
    ids = [skill.get("id", "") for skill in skills if isinstance(skill, dict)]
    names = [skill.get("name", "") for skill in skills if isinstance(skill, dict)]
    if duplicates := duplicate_values(ids):
        errors.append(f"duplicate skill ids: {sorted(duplicates)}")
    if duplicates := duplicate_values(names):
        errors.append(f"duplicate skill names: {sorted(duplicates)}")
    for index, skill in enumerate(skills):
        if not isinstance(skill, dict) or set(skill) != SKILL_FIELDS:
            errors.append(f"skill {index} has invalid fields")
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", skill["id"]):
            errors.append(f"skill {skill['name']} has invalid id")
        if skill["category"] not in SKILL_CATEGORIES:
            errors.append(f"skill {skill['name']} has invalid category")
        if skill["level"] not in SKILL_LEVELS:
            errors.append(f"skill {skill['name']} has invalid level")
    return set(names), errors
