"""Pydantic v2 models representing requirement cases and verification outcomes."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RequirementCase(BaseModel):
    """A test case validating a specific requirement."""
    case_id: str = Field(..., description="Unique ID matching convention")
    requirement_id: str = Field(..., description="Parent Requirement ID")
    requirement_type: str = Field(..., description="FR or NFR")
    title: str = Field(..., description="Concise test intent")
    description: str = Field(..., description="Detailed description")
    category: str = Field(..., description="Case category")
    priority: str = Field("P0", description="P0, P1, or P2")
    preconditions: list[str] = Field(default_factory=list)
    input_data: dict[str, Any] = Field(default_factory=dict)
    steps: list[str] = Field(default_factory=list)
    expected: Any = Field(..., description="Expected outcome details")
    negative: bool = Field(False, description="Is negative failure assertion")
    automation_level: str = Field("automated", description="automated, semi-automated, or manual")
    verification_method: str = Field("api_call", description="api_call, unit_test, file_scan, etc.")
    target_files: list[str] = Field(default_factory=list)
    target_endpoints: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class RequirementVerificationResult(BaseModel):
    """Execution status for a single requirement case."""
    case_id: str
    requirement_id: str
    requirement_type: str
    title: str
    status: str = Field("PASS", description="PASS or FAIL")
    message: str = Field("", description="Execution outcome logs")


class RequirementVerificationSummary(BaseModel):
    """Aggregated verification results."""
    total_fr_requirements: int
    total_nfr_requirements: int
    total_fr_cases: int
    total_nfr_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float
    requirements_with_less_than_50_cases: list[str]
    failed_requirements: list[str]
    security_findings: list[str]
    documentation_findings: list[str]
    final_verdict: str = Field("PASS", description="PASS or FAIL")
