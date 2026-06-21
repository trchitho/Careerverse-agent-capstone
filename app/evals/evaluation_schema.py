"""Strict contracts for deterministic local evaluation cases and results."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CaseType = Literal["normal", "edge", "security", "invalid"]
ExpectedStatus = Literal["success", "blocked", "validation_error"]


class EvaluationExpected(BaseModel):
    """Expected behavior and optional quality signals for one case."""

    model_config = ConfigDict(extra="forbid")

    status: ExpectedStatus
    top_k: int = Field(default=3, ge=1, le=10)
    expected_keywords: list[str] = Field(default_factory=list)
    expected_missing_skills_any: list[str] = Field(default_factory=list)
    required_response_fields: list[str] = Field(default_factory=list)
    expected_risk: Literal["none", "low", "medium", "high"] | None = None
    must_not_echo: list[str] = Field(default_factory=list)
