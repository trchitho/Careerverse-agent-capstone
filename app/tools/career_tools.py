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


def calculate_interest_score(
    user_interests: list[str] | None,
    career_recommended_for: list[str] | None,
) -> float:
    """Calculate deterministic interest overlap on a 0–100 scale."""
    interests = normalize_list(user_interests)
    tags = normalize_list(career_recommended_for)
    if not interests or not tags:
        return 0.0

    strengths = [
        max((_match_strength(interest, tag) for tag in tags), default=0.0)
        for interest in interests
    ]
    return round(clamp_score(sum(strengths) / len(strengths) * 100), 2)


def calculate_skill_score(
    user_skills: list[str] | None,
    career_required_skills: list[str] | None,
) -> float:
    """Calculate required-skill coverage using canonical aliases."""
    required = _canonicalize_skills(career_required_skills)
    if not required:
        return 0.0
    user = _canonicalize_skills(user_skills)
    matched = set(required) & set(user)
    return round(clamp_score(len(matched) / len(required) * 100), 2)


def _field_tokens(value: object) -> set[str]:
    """Collect tokens from a string or list of strings."""
    if isinstance(value, str):
        return tokenize_text(value)
    if isinstance(value, list):
        return set().union(*(tokenize_text(str(item)) for item in value))
    return set()


def calculate_goal_score(user_goal: str | None, career: dict[str, Any]) -> float:
    """Score weighted career-goal relevance across explainable fields."""
    goal_tokens = tokenize_text(user_goal)
    if not goal_tokens:
        return 0.0
    weighted_fields = (
        (career.get("title", ""), 0.30),
        (career.get("recommended_for", []), 0.25),
        (career.get("family", ""), 0.15),
        (career.get("description", ""), 0.10),
        (career.get("daily_work", []), 0.08),
        (career.get("sample_projects", []), 0.07),
        (career.get("explanation", ""), 0.05),
    )
    score = 0.0
    for value, weight in weighted_fields:
        field_tokens = _field_tokens(value)
        score += len(goal_tokens & field_tokens) / len(goal_tokens) * weight * 100
    return round(clamp_score(score), 2)


def build_search_text(career: dict[str, Any]) -> str:
    """Build a stable search representation from relevant career fields."""
    fields = [
        career.get("title", ""),
        career.get("description", ""),
        career.get("family", ""),
        career.get("explanation", ""),
        *career.get("recommended_for", []),
        *career.get("daily_work", []),
        *career.get("sample_projects", []),
    ]
    return normalize_text(" ".join(str(value) for value in fields))


def extract_profile_fields(profile: object) -> tuple[list[str], list[str], str]:
    """Extract matching fields from a mapping or Pydantic model."""
    if hasattr(profile, "model_dump"):
        payload = profile.model_dump()
    elif isinstance(profile, dict):
        payload = profile
    else:
        raise TypeError("profile must be a dictionary or Pydantic model")
    interests = normalize_list(payload.get("interests"))
    skills = normalize_list(payload.get("skills"))
    goal = str(payload.get("career_goal") or "").strip()
    return interests, skills, goal


def calculate_missing_skills(
    user_skills: list[str] | None,
    required_skills: list[str] | None,
) -> list[str]:
    """Return unmatched required skills in source order."""
    user = _canonicalize_skills(user_skills)
    missing: list[str] = []
    seen: set[str] = set()
    for required in normalize_list(required_skills):
        canonical = _canonicalize_skills([required])
        key = next(iter(canonical), normalize_text(required))
        if key not in user and key not in seen:
            seen.add(key)
            missing.append(required)
    return missing


def _matched_skills(
    user_skills: list[str], required_skills: list[str]
) -> list[str]:
    """Return canonical matched skills in career requirement order."""
    user = _canonicalize_skills(user_skills)
    matched: list[str] = []
    for required in normalize_list(required_skills):
        canonical = _canonicalize_skills([required])
        key = next(iter(canonical), normalize_text(required))
        if key in user:
            matched.append(required)
    return matched


def _matched_interests(
    interests: list[str], career_tags: list[str]
) -> list[str]:
    """Return user interests with meaningful overlap to career tags."""
    return [
        interest
        for interest in interests
        if max((_match_strength(interest, tag) for tag in career_tags), default=0.0)
        >= 0.65
    ]


def build_matched_reasons(
    interests: list[str],
    matched_skills: list[str],
    goal_score: float,
    career: dict[str, Any],
) -> list[str]:
    """Build concise, truthful explanations for one recommendation."""
    reasons = [
        f"Matches your interest in {interest}."
        for interest in _matched_interests(interests, career.get("recommended_for", []))[:2]
    ]
    reasons.extend(
        f"Matches your skill: {skill}." for skill in matched_skills[:2]
    )
    if goal_score > 0:
        reasons.append(f"Your career goal aligns with {career.get('title', 'this role')}.")
    if not reasons:
        reasons.append(
            "This role appears because it has limited overlap with your stated profile."
        )
    return reasons[:6]


def _score_career(
    career: dict[str, Any],
    interests: list[str],
    skills: list[str],
    goal: str,
) -> dict[str, Any]:
    """Score and format one career without mutating source data."""
    required = normalize_list(career.get("required_skills"))
    matched = _matched_skills(skills, required)
    interest_score = calculate_interest_score(
        interests, career.get("recommended_for")
    )
    skill_score = calculate_skill_score(skills, required)
    goal_score = calculate_goal_score(goal, career)
    total = round(clamp_score(
        interest_score * SCORE_WEIGHTS["interest"]
        + skill_score * SCORE_WEIGHTS["skill"]
        + goal_score * SCORE_WEIGHTS["goal"]
    ), 2)
    return {
        "career_id": str(career.get("id", "")),
        "title": str(career.get("title", "")),
        "family": career.get("family"),
        "level": career.get("level"),
        "description": str(career.get("description", "")),
        "score": total,
