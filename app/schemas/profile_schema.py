"""Public request and response schemas for CareerVerse Agent."""

import re
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

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
    career_goal: str = Field(min_length=1, max_length=300)
    preferred_learning_style: LearningStyle = "mixed"
    language: SupportedLanguage = "en"
    experience_level: ExperienceLevel = "university"
    time_budget_hours_per_week: int = Field(default=8, ge=1, le=80)

    @field_validator("interests", "skills", mode="before")
    @classmethod
    def normalize_lists(cls, value: object, info: ValidationInfo) -> list[str]:
        """Normalize interests and skills before length constraints."""
        return normalize_unique_strings(value, info.field_name)

    @field_validator("career_goal")
    @classmethod
    def reject_obvious_prompt_injection(cls, value: str) -> str:
        """Reject explicit attempts to override or expose system controls."""
        normalized = re.sub(r"\s+", " ", value).casefold()
        if any(pattern in normalized for pattern in PROMPT_INJECTION_PATTERNS):
            raise ValueError("career_goal contains a disallowed instruction pattern")
        return value


class UserProfileSummary(StrictSchema):
    """Normalized profile returned by validation and recommendation APIs."""

    name: str
    education: str
    interests: list[str]
    skills: list[str]
    career_goal: str
    preferred_learning_style: LearningStyle
    language: SupportedLanguage
    experience_level: ExperienceLevel
    time_budget_hours_per_week: int = Field(ge=1, le=80)


class CareerRecommendation(StrictSchema):
    """Ranked career option produced by a future recommendation engine."""

    career_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    family: str | None = None
    level: str | None = None
    description: str = Field(min_length=1)
    score: float = Field(ge=0, le=100)
    matched_reasons: list[str] = Field(min_length=1)
    required_skills: list[str] = Field(min_length=1)
    nice_to_have_skills: list[str] = Field(default_factory=list)
    missing_skills_preview: list[str] = Field(default_factory=list)
    market_relevance: dict[str, str] | None = None
    explanation: str | None = None


class SkillGapResult(StrictSchema):
    """Structured comparison between current and required skills."""

    matched_skills: list[str]
    missing_skills: list[str]
    priority_skills: list[str]
    readiness_score: float = Field(ge=0, le=100)
