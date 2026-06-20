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


def validate_careers(
    careers: Any, skill_names: set[str]
) -> tuple[set[str], set[str], list[str]]:
    """Validate career records and skill references."""
    errors: list[str] = []
    if not isinstance(careers, list) or len(careers) < 80:
        return set(), set(), ["careers.json must contain at least 80 records"]
    ids = [career.get("id", "") for career in careers if isinstance(career, dict)]
    titles = [career.get("title", "") for career in careers if isinstance(career, dict)]
    if duplicates := duplicate_values(ids):
        errors.append(f"duplicate career ids: {sorted(duplicates)}")
    if duplicates := duplicate_values(titles):
        errors.append(f"duplicate career titles: {sorted(duplicates)}")
    for index, career in enumerate(careers):
        if not isinstance(career, dict) or set(career) != CAREER_FIELDS:
            errors.append(f"career {index} has invalid fields")
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", career["id"]):
            errors.append(f"career {career['title']} has invalid id")
        if career["family"] not in CAREER_FAMILIES:
            errors.append(f"career {career['id']} has invalid family")
        if career["level"] not in CAREER_LEVELS:
            errors.append(f"career {career['id']} has invalid level")
        if career["market_relevance"].get("level") not in MARKET_LEVELS:
            errors.append(f"career {career['id']} has invalid market relevance")
        if career["learning_difficulty"].get("level") not in DIFFICULTY_LEVELS:
            errors.append(f"career {career['id']} has invalid learning difficulty")
        if not 6 <= len(career["required_skills"]) <= 12:
            errors.append(f"career {career['id']} has invalid required skill count")
        if not 4 <= len(career["nice_to_have_skills"]) <= 10:
            errors.append(f"career {career['id']} has invalid optional skill count")
        if not career["recommended_for"]:
            errors.append(f"career {career['id']} has no recommendation tags")
        referenced = set(career["required_skills"] + career["nice_to_have_skills"])
        if missing := referenced - skill_names:
            errors.append(f"career {career['id']} missing skills: {sorted(missing)}")
    return set(ids), set(titles), errors


def validate_week(
    career_id: str, plan_name: str, week: Any, skill_names: set[str]
) -> list[str]:
    """Validate one roadmap week and its skill references."""
    if not isinstance(week, dict) or set(week) != WEEK_FIELDS:
        return [f"{career_id} {plan_name} contains an invalid week"]
    errors: list[str] = []
    if not 2 <= len(week["learning_goals"]) <= 4:
        errors.append(f"{career_id} week {week['week']} has invalid learning goals")
    if not 3 <= len(week["tasks"]) <= 5:
        errors.append(f"{career_id} week {week['week']} has invalid task count")
    if not 2 <= len(week["skills_practiced"]) <= 6:
        errors.append(f"{career_id} week {week['week']} has invalid skills count")
    if missing := set(week["skills_practiced"]) - skill_names:
        errors.append(
            f"{career_id} week {week['week']} references skills: {sorted(missing)}"
        )
    return errors


def validate_plan(
    career_id: str, name: str, plan: Any, expected_weeks: int, skill_names: set[str]
) -> list[str]:
    """Validate roadmap week count, order, and week records."""
    if not isinstance(plan, list) or len(plan) != expected_weeks:
        return [f"{career_id} {name} must have {expected_weeks} weeks"]
