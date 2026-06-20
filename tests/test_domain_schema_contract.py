"""Contract tests between Pydantic domain schemas and generated JSON."""

import json
from pathlib import Path

from app.schemas.domain_schema import CareerProfile, CareerRoadmap, SkillProfile

DATA_DIR = Path(__file__).resolve().parents[1] / "app" / "data"


def load_json(filename: str) -> object:
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


def test_career_profiles_match_schema() -> None:
    careers = load_json("careers.json")
    assert isinstance(careers, list)

    samples = careers[:5] + careers[-5:]
    assert all(CareerProfile.model_validate(item) for item in samples)


def test_skill_profiles_match_schema() -> None:
    skills = load_json("skills.json")
    assert isinstance(skills, list)

    samples = skills[:10] + skills[-10:]
    assert all(SkillProfile.model_validate(item) for item in samples)
