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

    def __init__(
        self,
        skill_gap_agent: SkillGapAgent | None = None,
        roadmap_agent: RoadmapAgent | None = None,
    ) -> None:
        self.skill_gap_agent = skill_gap_agent or SkillGapAgent()
        self.roadmap_agent = roadmap_agent or RoadmapAgent()

    @staticmethod
    def _normalize_profile(profile: object) -> UserProfileRequest:
        """Return a validated profile copy from a mapping or Pydantic model."""
        if hasattr(profile, "model_dump"):
            payload = profile.model_dump()
        elif isinstance(profile, dict):
            payload = deepcopy(profile)
        else:
            raise ValueError("Profile must be a dictionary or Pydantic model.")
        try:
            return UserProfileRequest.model_validate(payload)
        except ValidationError as error:
            raise ValueError("Profile is invalid and could not be processed.") from error

    def run(self, profile: object, top_k: int = 3) -> dict[str, object]:
        """Run the complete deterministic multi-agent workflow."""
        normalized = self._normalize_profile(profile)
        recommendations = recommend_careers(normalized, top_k=top_k)
        if not recommendations:
            raise ValueError(
                "No career recommendations could be generated for the provided profile."
            )
        top_career = recommendations[0]
        skill_gap = self.skill_gap_agent.analyze(
            user_skills=normalized.skills,
            required_skills=top_career["required_skills"],
            nice_to_have_skills=top_career["nice_to_have_skills"],
        )
        roadmap = self.roadmap_agent.get_roadmap(
            career_id=str(top_career["career_id"]),
            career_title=str(top_career["title"]),
            missing_skills=skill_gap["priority_skills"],
        )
        payload = {
            "user_summary": UserProfileSummary.model_validate(
                normalized.model_dump()
            ).model_dump(),
            "top_recommendations": recommendations,
            "skill_gap": skill_gap,
            "personalized_roadmap": roadmap,
            "safety_notice": SAFETY_NOTICE,
            "course_concepts_demonstrated": COURSE_CONCEPTS,
        }
        return AgentRecommendationResponse.model_validate(payload).model_dump()
