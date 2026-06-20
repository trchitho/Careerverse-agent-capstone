"""Public request and response schemas for CareerVerse Agent."""

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SupportedLanguage = Literal["en", "vi"]
LearningStyle = Literal["visual", "reading", "hands_on", "project_based", "mixed"]
ExperienceLevel = Literal[
    "high_school", "university", "fresher", "junior", "career_changer", "self_taught"
]

SUPPORTED_LANGUAGES = {"en", "vi"}
SUPPORTED_LEARNING_STYLES = {"visual", "reading", "hands_on", "project_based", "mixed"}
SUPPORTED_EXPERIENCE_LEVELS = {
    "high_school", "university", "fresher", "junior", "career_changer", "self_taught"
}
PROMPT_INJECTION_PATTERNS = (
    "ignore previous instructions", "reveal system prompt", "show api key",
    "bypass security", "disable guardrails", "print secrets",
    "override developer instructions",
)


class StrictSchema(BaseModel):
    """Base model for strict public API contracts."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


def normalize_unique_strings(value: object, field_name: str) -> list[str]:
    """Normalize a string list while preserving first-occurrence casing."""
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")

    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str):
            raise ValueError(f"{field_name} items must be strings")
        cleaned = re.sub(r"\s+", " ", item).strip()
        if not cleaned:
            raise ValueError(f"{field_name} must not contain blank items")
        key = cleaned.casefold()
        if key not in seen:
            seen.add(key)
            normalized.append(cleaned)
    return normalized


class UserProfileRequest(StrictSchema):
    """Validated and normalized career guidance profile input."""

    name: str = Field(min_length=1, max_length=80)
    education: str = Field(min_length=1, max_length=200)
    interests: list[str] = Field(min_length=1, max_length=20)
    skills: list[str] = Field(min_length=1, max_length=50)
