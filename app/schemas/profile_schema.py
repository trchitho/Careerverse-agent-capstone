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
