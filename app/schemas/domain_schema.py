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
