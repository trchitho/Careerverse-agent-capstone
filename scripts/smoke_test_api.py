"""Offline FastAPI smoke test for all critical CareerVerse endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

PROFILE = {
    "name": "Demo User",
    "education": "Final-year IT student",
    "interests": ["AI", "web development", "product building"],
    "skills": ["Python", "React", "SQL"],
    "career_goal": "Become an AI full-stack developer",
    "preferred_learning_style": "project_based",
    "language": "en",
    "experience_level": "university",
    "time_budget_hours_per_week": 8,
}


def main() -> int:
    """Run endpoint checks and return nonzero when a critical route fails."""
    client = TestClient(app)
    cases = [
        ("GET /", lambda: client.get("/")),
        ("GET /metadata", lambda: client.get("/metadata")),
        ("POST /profiles/validate", lambda: client.post("/profiles/validate", json=PROFILE)),
