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


class CareerProfile(DomainSchema):
    """Validated production career profile."""

    id: str
    title: str = Field(min_length=1)
    family: CareerFamily
    level: CareerLevel
    description: str = Field(min_length=1)
    target_users: list[str] = Field(min_length=1)
    required_skills: list[str] = Field(min_length=6, max_length=12)
    nice_to_have_skills: list[str] = Field(min_length=4, max_length=10)
    recommended_for: list[str] = Field(min_length=1)
    avoid_if: list[str] = Field(min_length=2, max_length=5)
    sample_projects: list[str] = Field(min_length=2, max_length=5)
    daily_work: list[str] = Field(min_length=3, max_length=6)
    growth_paths: list[str] = Field(min_length=2, max_length=5)
    market_relevance: MarketRelevance
    learning_difficulty: LearningDifficulty
    personality_fit: PersonalityFit
    explanation: str = Field(min_length=1)
    safety_note: str = Field(min_length=1)

    _validate_id = field_validator("id")(require_snake_case)


class SkillProfile(DomainSchema):
    """Validated skill catalog record."""

    id: str
    name: str = Field(min_length=1)
    category: SkillCategory
    level: SkillLevel
    aliases: list[str] = Field(min_length=1)
    description: str = Field(min_length=1)
    used_in_roles: list[str] = Field(min_length=1)
    related_skills: list[str] = Field(min_length=1)
    learning_resources_keywords: list[str] = Field(min_length=1)
    assessment_hint: str = Field(min_length=1)

    _validate_id = field_validator("id")(require_snake_case)


class DomainRoadmapWeek(DomainSchema):
    """Validated roadmap week stored in the domain dataset."""

    week: int = Field(ge=1, le=8)
    focus: str = Field(min_length=1, max_length=200)
    learning_goals: list[str] = Field(min_length=2, max_length=4)
    tasks: list[str] = Field(min_length=3, max_length=5)
    deliverable: str = Field(min_length=1, max_length=300)
    skills_practiced: list[str] = Field(min_length=2, max_length=6)
    checkpoint: str = Field(min_length=1, max_length=300)
