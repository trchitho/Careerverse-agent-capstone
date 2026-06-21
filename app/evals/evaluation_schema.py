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


class EvaluationCase(BaseModel):
    """One synthetic evaluation profile and its expected behavior."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    type: CaseType
    description: str = Field(min_length=1)
    input_profile: dict[str, object]
    expected: EvaluationExpected


class EvaluationResult(BaseModel):
    """Machine-readable result for one evaluation case."""

    case_id: str
    case_type: CaseType
    passed: bool
    message: str


class EvaluationSummary(BaseModel):
    """Aggregate evaluation result."""

    total: int
    passed: int
    failed: int
    skipped: int = 0
    score: float = Field(ge=0, le=100)
