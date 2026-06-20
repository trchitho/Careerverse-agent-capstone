"""Multi-agent career guidance workflow orchestrator."""

from copy import deepcopy

from pydantic import ValidationError

from app.agents.roadmap_agent import RoadmapAgent
from app.agents.skill_gap_agent import SkillGapAgent
from app.schemas.profile_schema import (
    AgentRecommendationResponse,
    UserProfileRequest,
    UserProfileSummary,
)
from app.tools.career_tools import recommend_careers

SAFETY_NOTICE = (
    "This system provides educational career guidance only. It does not "
    "guarantee employment outcomes or replace professional counseling."
)
COURSE_CONCEPTS = [
    "Multi-agent system",
    "Deterministic scoring engine",
    "MCP-style tool integration ready",
    "Agent Skills",
    "Security and input validation",
    "Local evaluation pipeline",
    "FastAPI deployability",
]


class CareerAdvisorAgent:
    """Coordinate recommendation, skill gap, and roadmap agents."""
