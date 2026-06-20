"""Unit tests for profile request and response validation."""

import pytest
from pydantic import ValidationError

from app.schemas.profile_schema import UserProfileRequest


def valid_payload() -> dict[str, object]:
    return {
        "name": "Tho",
        "education": "Final-year IT student",
        "interests": ["AI", "web development"],
        "skills": ["Python", "React", "SQL"],
        "career_goal": "Become an AI full-stack developer",
    }


def test_valid_profile_passes() -> None:
    profile = UserProfileRequest.model_validate(valid_payload())

    assert profile.language == "en"
    assert profile.time_budget_hours_per_week == 8


def test_whitespace_is_stripped() -> None:
    payload = valid_payload() | {"name": "  Tho  ", "education": "  IT student  "}

    profile = UserProfileRequest.model_validate(payload)

    assert profile.name == "Tho"
    assert profile.education == "IT student"


def test_duplicate_interests_are_normalized() -> None:
    payload = valid_payload() | {"interests": [" AI ", "ai", "Web   Development"]}

    profile = UserProfileRequest.model_validate(payload)

    assert profile.interests == ["AI", "Web Development"]


def test_duplicate_skills_are_normalized() -> None:
    payload = valid_payload() | {"skills": ["Python", " python ", "React"]}

    profile = UserProfileRequest.model_validate(payload)

    assert profile.skills == ["Python", "React"]


@pytest.mark.parametrize("field", ["interests", "skills"])
def test_empty_profile_lists_are_rejected(field: str) -> None:
    with pytest.raises(ValidationError):
        UserProfileRequest.model_validate(valid_payload() | {field: []})


@pytest.mark.parametrize("field", ["interests", "skills"])
def test_blank_profile_list_items_are_rejected(field: str) -> None:
    with pytest.raises(ValidationError):
        UserProfileRequest.model_validate(valid_payload() | {field: ["   "]})
