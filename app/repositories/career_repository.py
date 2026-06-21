"""JSON-backed career repository implementation."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.core.exceptions import ResourceNotFoundError

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
REQUIRED_CAREER_FIELDS = {
    "id",
    "title",
    "description",
    "required_skills",
    "recommended_for",
}


@lru_cache(maxsize=1)
def _cached_load_careers(data_dir: Path) -> list[dict[str, Any]]:
    path = data_dir / "careers.json"
    if not path.is_file():
        raise FileNotFoundError(f"Domain data file not found: {path}")
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, list):
        raise ValueError("careers.json root must be a JSON array")
    records: list[dict[str, Any]] = []
    for index, record in enumerate(payload):
        if not isinstance(record, dict):
            raise ValueError(f"careers.json record {index} must be an object")
        missing = REQUIRED_CAREER_FIELDS - set(record)
        if missing:
            raise ValueError(
                f"careers.json record {index} is missing fields: {sorted(missing)}"
            )
        records.append(record)
    return records


class JsonCareerRepository:
    """Repository accessing careers from local JSON dataset."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or DATA_DIR

    def _load(self) -> list[dict[str, Any]]:
        return _cached_load_careers(self.data_dir)

    def list_careers(self) -> list[dict[str, Any]]:
        """List all careers in the JSON dataset."""
        from app.tools.career_tools import load_careers
        return load_careers()

    def get_career_by_id(self, career_id: str) -> dict[str, Any]:
        """Retrieve a career by its ID. Raise ResourceNotFoundError if missing."""
        normalized = career_id.strip().casefold()
        if not normalized:
            raise ValueError("career_id must not be blank")
        for career in self.list_careers():
            if str(career.get("id", "")).strip().casefold() == normalized:
                return career
        raise ResourceNotFoundError(f"Career with ID '{career_id}' not found in catalog.")

    def search_careers(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search careers matching the query string in title/description."""
        normalized_query = query.strip().casefold()
        if not normalized_query:
            return []
        matches = []
        for career in self.list_careers():
            title = str(career.get("title", "")).casefold()
            desc = str(career.get("description", "")).casefold()
            if normalized_query in title or normalized_query in desc:
                matches.append(career)
        return matches[:limit]
