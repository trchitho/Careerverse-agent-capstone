"""Unit tests for deterministic security and responsible AI tools."""

from copy import deepcopy

import pytest

from app.tools.safety_tools import (
    detect_prompt_injection,
    get_safety_notice,
    redact_sensitive_text,
    validate_profile_safety,
)

EXPECTED_NOTICE = (
    "This system provides educational career guidance only. "
    "It does not guarantee employment outcomes or replace professional counseling."
)


def normal_profile() -> dict[str, object]:
    return {
        "name": "Demo User",
        "education": "Final-year IT student",
        "interests": ["AI", "web development"],
        "skills": ["Python", "React"],
        "career_goal": "Build practical AI-enabled web products",
    }


def test_safety_notice_is_canonical() -> None:
    assert get_safety_notice() == EXPECTED_NOTICE
