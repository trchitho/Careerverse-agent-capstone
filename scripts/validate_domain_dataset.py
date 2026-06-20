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
