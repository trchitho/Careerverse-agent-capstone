"""JSON-backed roadmap repository implementation."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.core.exceptions import ResourceNotFoundError

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@lru_cache(maxsize=1)
def _cached_load_roadmaps(data_dir: Path) -> dict[str, Any]:
    path = data_dir / "roadmaps.json"
    if not path.is_file():
        raise FileNotFoundError(f"Domain data file not found: {path}")
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError("roadmaps.json root must be a JSON object")
    return payload


class JsonRoadmapRepository:
    """Repository accessing roadmaps from local JSON dataset."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or DATA_DIR

    def _load(self) -> dict[str, Any]:
        return _cached_load_roadmaps(self.data_dir)

    def list_roadmaps(self) -> dict[str, Any]:
        """List all roadmaps in the JSON dataset."""
        import copy
        return copy.deepcopy(self._load())

    def get_roadmap_by_career_id(self, career_id: str) -> dict[str, Any]:
        """Retrieve roadmap by career ID. Raise ResourceNotFoundError if missing."""
        normalized = career_id.strip()
        if not normalized:
            raise ValueError("career_id must not be blank")
        roadmaps = self.list_roadmaps()
        if normalized not in roadmaps:
            raise ResourceNotFoundError(f"Roadmap not found for career ID '{career_id}'.")
        return roadmaps[normalized]
