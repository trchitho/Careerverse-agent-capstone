"""Contract tests for the production Career Advisor Skill."""

from pathlib import Path

SKILL_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "skills"
    / "career_advisor"
    / "SKILL.md"
)

REQUIRED_SECTIONS = [
    "Purpose",
    "When to Use",
    "When Not to Use",
    "Required Inputs",
    "Workflow Overview",
    "Tool Usage",
    "Output Contract",
    "Safety and Responsible AI Rules",
    "Failure Handling",
    "Example Input",
    "Example Output",
]


def test_career_advisor_skill_exists_and_has_title() -> None:
    assert SKILL_PATH.is_file()
    assert "# Career Advisor Skill" in SKILL_PATH.read_text(encoding="utf-8")


def test_career_advisor_skill_has_required_sections() -> None:
    content = SKILL_PATH.read_text(encoding="utf-8")

    for section in REQUIRED_SECTIONS:
        assert section in content


def test_career_advisor_skill_has_safety_and_tool_contracts() -> None:
    content = SKILL_PATH.read_text(encoding="utf-8")
    required_phrases = [
        "does not guarantee employment outcomes",
        "AgentRecommendationResponse",
        "CareerAdvisorAgent",
        "SkillGapAgent",
        "RoadmapAgent",
        "MCP-style",
        "UserProfileRequest",
    ]

    for phrase in required_phrases:
        assert phrase in content
