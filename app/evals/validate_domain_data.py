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
