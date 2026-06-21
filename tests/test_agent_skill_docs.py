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
