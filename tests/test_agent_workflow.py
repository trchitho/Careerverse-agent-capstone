"""Production workflow tests spanning agents, schemas, API, and MCP routes."""

from copy import deepcopy

from fastapi.testclient import TestClient

from app.agents import CareerAdvisorAgent
from app.main import app
from app.schemas import AgentRecommendationResponse
from app.tools.safety_tools import get_safety_notice

client = TestClient(app)


def profile_payload() -> dict[str, object]:
    return {
        "name": "Evaluation User",
        "education": "Final-year IT student",
        "interests": ["AI", "web development", "product building"],
        "skills": ["Python", "React", "SQL"],
        "career_goal": "Become an AI full-stack developer",
        "preferred_learning_style": "project_based",
        "language": "en",
        "experience_level": "university",
        "time_budget_hours_per_week": 8,
    }
