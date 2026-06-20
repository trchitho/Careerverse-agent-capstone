"""Deterministic, explainable career recommendation tools."""

import json
import re
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_SAFETY_NOTE = (
    "This recommendation is educational guidance only and does not guarantee "
    "employment outcomes."
)
SCORE_WEIGHTS = {"interest": 0.35, "skill": 0.45, "goal": 0.20}
REQUIRED_CAREER_FIELDS = {
    "id", "title", "description", "required_skills", "recommended_for"
}
REQUIRED_SKILL_FIELDS = {"id", "name", "category", "level"}


def _load_json(filename: str) -> object:
    """Load one local JSON dataset with explicit file errors."""
    path = DATA_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"Domain data file not found: {path}")
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _validate_records(
    payload: object, filename: str, required_fields: set[str]
) -> list[dict[str, Any]]:
    """Validate a dataset root and minimum record fields."""
    if not isinstance(payload, list):
        raise ValueError(f"{filename} root must be a JSON array")
    records: list[dict[str, Any]] = []
    for index, record in enumerate(payload):
        if not isinstance(record, dict):
            raise ValueError(f"{filename} record {index} must be an object")
        missing = required_fields - set(record)
        if missing:
            raise ValueError(
                f"{filename} record {index} is missing fields: {sorted(missing)}"
            )
        records.append(record)
    return records


@lru_cache(maxsize=1)
def load_careers() -> list[dict[str, Any]]:
    """Load and minimally validate the cached career catalog."""
    return _validate_records(
        _load_json("careers.json"), "careers.json", REQUIRED_CAREER_FIELDS
    )
