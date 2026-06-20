"""Roadmap retrieval and safe fallback agent."""

import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.schemas.profile_schema import RoadmapResult
from app.tools.career_tools import normalize_list

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "roadmaps.json"
ROADMAP_SAFETY_NOTE = (
    "This roadmap is educational guidance only and should be adapted to the "
    "learner's context."
)


class RoadmapAgent:
    """Retrieve production roadmaps and produce schema-valid fallbacks."""

    @staticmethod
    @lru_cache(maxsize=1)
    def load_roadmaps() -> dict[str, dict[str, Any]]:
        """Load and cache the local roadmap catalog."""
        if not DATA_PATH.is_file():
            raise FileNotFoundError(f"Roadmap data file not found: {DATA_PATH}")
        with DATA_PATH.open(encoding="utf-8") as file:
            payload = json.load(file)
        if not isinstance(payload, dict):
            raise ValueError("roadmaps.json root must be a JSON object")
        return payload
