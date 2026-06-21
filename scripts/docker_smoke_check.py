"""Docker smoke check script using Python stdlib."""

from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

IMAGE_NAME = "careerverse-agent-api:smoke"
CONTAINER_NAME = "careerverse-agent-api-smoke"
PORT = 18000
URL = f"http://127.0.0.1:{PORT}"

DEMO_PROFILE = {
    "name": "Docker Demo User",
    "education": "Final-year IT student",
    "interests": ["AI", "web development"],
    "skills": ["Python", "React", "SQL"],
    "career_goal": "Become an AI full-stack developer",
    "preferred_learning_style": "project_based",
    "language": "en",
    "experience_level": "university",
    "time_budget_hours_per_week": 8
}
