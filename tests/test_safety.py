"""Integration-level safety tests for evaluation and recommendation workflows."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.schemas import UserProfileRequest
from app.tools.safety_tools import (
    get_safety_notice,
    redact_sensitive_text,
    validate_profile_safety,
)

ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def safe_profile() -> dict[str, object]:
    return {
        "name": "Safety Demo",
        "education": "IT student",
        "interests": ["AI", "web development"],
        "skills": ["Python", "React"],
        "career_goal": "Build useful AI web products",
    }
