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
