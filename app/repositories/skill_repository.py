"""JSON-backed skill repository implementation."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.core.exceptions import ResourceNotFoundError

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
REQUIRED_SKILL_FIELDS = {"id", "name", "category", "level"}


@lru_cache(maxsize=1)
def _cached_load_skills(data_dir: Path) -> list[dict[str, Any]]:
    path = data_dir / "skills.json"
    if not path.is_file():
        raise FileNotFoundError(f"Domain data file not found: {path}")
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, list):
        raise ValueError("skills.json root must be a JSON array")
    records: list[dict[str, Any]] = []
    for index, record in enumerate(payload):
        if not isinstance(record, dict):
            raise ValueError(f"skills.json record {index} must be an object")
        missing = REQUIRED_SKILL_FIELDS - set(record)
        if missing:
            raise ValueError(
                f"skills.json record {index} is missing fields: {sorted(missing)}"
            )
        records.append(record)
    return records


class JsonSkillRepository:
    """Repository accessing skill metadata from local JSON dataset."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or DATA_DIR

    def _load(self) -> list[dict[str, Any]]:
        return _cached_load_skills(self.data_dir)

    def list_skills(self) -> list[dict[str, Any]]:
        """List all skills in the JSON dataset."""
        from app.tools.career_tools import load_skills
        return load_skills()

    def get_skill_by_name(self, skill_name: str) -> dict[str, Any]:
        """Retrieve skill metadata by name, ID or alias. Raise ResourceNotFoundError if missing."""
        normalized = skill_name.strip().casefold()
        if not normalized:
            raise ValueError("skill_name must not be blank")
        for skill in self.list_skills():
            candidates = [
                str(skill.get("id", "")).strip().casefold(),
                str(skill.get("name", "")).strip().casefold(),
                *[str(alias).strip().casefold() for alias in skill.get("aliases", [])],
            ]
            if normalized in candidates:
                return skill
        raise ResourceNotFoundError(f"Skill with name/alias '{skill_name}' not found.")
