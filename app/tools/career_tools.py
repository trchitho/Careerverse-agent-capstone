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


@lru_cache(maxsize=1)
def load_skills() -> list[dict[str, Any]]:
    """Load and minimally validate the cached skill catalog."""
    return _validate_records(
        _load_json("skills.json"), "skills.json", REQUIRED_SKILL_FIELDS
    )


def normalize_text(value: str | None) -> str:
    """Normalize text while preserving useful technology punctuation."""
    if value is None:
        return ""
    lowered = value.casefold().strip()
    cleaned = re.sub(r"[^\w\s+#./-]", " ", lowered, flags=re.UNICODE)
    return re.sub(r"\s+", " ", cleaned).strip()


def normalize_list(values: list[str] | None) -> list[str]:
    """Clean and stably deduplicate human-readable string values."""
    result: list[str] = []
    seen: set[str] = set()
    for value in values or []:
        cleaned = re.sub(r"\s+", " ", value).strip()
        key = normalize_text(cleaned)
        if cleaned and key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result


def tokenize_text(value: str | None) -> set[str]:
    """Return stable normalized tokens for lightweight matching."""
    return {
        token
        for token in normalize_text(value).split()
        if token and token not in STOPWORDS
    }


STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "build", "career", "for", "in",
    "is", "of", "on", "or", "the", "to", "with", "work", "want",
    "become", "developer", "engineer", "role", "using", "my", "i",
    "và", "là", "của", "cho", "trong", "với", "muốn", "trở", "thành",
}


@lru_cache(maxsize=1)
def load_skill_alias_index() -> dict[str, str]:
    """Map normalized names and aliases to canonical skill names."""
    aliases: dict[str, str] = {}
    for skill in load_skills():
        canonical = str(skill["name"])
        candidates = [canonical, *skill.get("aliases", [])]
        for candidate in candidates:
            key = normalize_text(str(candidate))
            if key:
                aliases.setdefault(key, canonical)
    return aliases


def _canonicalize_skills(values: list[str] | None) -> dict[str, str]:
    """Return normalized canonical keys mapped to display names."""
    alias_index = load_skill_alias_index()
    canonical: dict[str, str] = {}
    for value in normalize_list(values):
        normalized = normalize_text(value)
        display = alias_index.get(normalized, value)
        canonical.setdefault(normalize_text(display), display)
    return canonical


def clamp_score(
    value: float, min_value: float = 0.0, max_value: float = 100.0
) -> float:
    """Clamp a score into an inclusive numeric range."""
    return max(min_value, min(max_value, value))


def _match_strength(left: str, right: str) -> float:
    """Score exact, token-overlap, and safe substring text matches."""
    left_normalized = normalize_text(left)
    right_normalized = normalize_text(right)
    if not left_normalized or not right_normalized:
        return 0.0
    if left_normalized == right_normalized:
        return 1.0
    left_tokens = tokenize_text(left_normalized)
    right_tokens = tokenize_text(right_normalized)
    if left_tokens and right_tokens and left_tokens & right_tokens:
        return 0.65
    if min(len(left_normalized), len(right_normalized)) >= 3:
        if left_normalized in right_normalized or right_normalized in left_normalized:
            return 0.35
    return 0.0
