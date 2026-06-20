"""Pydantic contracts for the generated CareerVerse domain datasets."""

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

CareerFamily = Literal[
    "Software Engineering", "AI / ML / Agent", "Data", "Cloud / DevOps",
    "Security", "Product / Business", "Education / Social Good",
    "Tech Support / Operations",
]
CareerLevel = Literal["entry", "entry_to_mid", "mid", "advanced"]
MarketLevel = Literal["medium", "high", "emerging"]
DifficultyLevel = Literal["low", "medium", "high"]
SkillLevel = Literal["beginner", "intermediate", "advanced"]
SkillCategory = Literal[
    "frontend", "backend", "ai", "data", "cloud", "security", "soft-skill",
    "product", "testing", "devops", "database", "architecture", "documentation",
]


class DomainSchema(BaseModel):
    """Strict base contract for local domain records."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


def require_snake_case(value: str) -> str:
    """Validate stable snake_case identifiers."""
    if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        raise ValueError("id must use snake_case")
    return value


class MarketRelevance(DomainSchema):
    """Qualitative market context without outcome guarantees."""

    level: MarketLevel
    reason: str = Field(min_length=1)


class LearningDifficulty(DomainSchema):
    """Qualitative learning difficulty and rationale."""

    level: DifficultyLevel
    reason: str = Field(min_length=1)


class PersonalityFit(DomainSchema):
    """Non-clinical traits that may affect role fit."""

    good_fit_traits: list[str] = Field(min_length=1)
    may_struggle_if: list[str] = Field(min_length=1)
