"""Tests for the offline CareerVerse domain data catalog."""

from app.evals.validate_domain_data import load_json, validate_domain_data


def test_domain_data_passes_all_validation() -> None:
    assert validate_domain_data() == []


def test_required_catalog_sizes() -> None:
    careers = load_json("careers.json")
    skills = load_json("skills.json")
    roadmaps = load_json("roadmaps.json")

    assert len(careers) >= 80
    assert len(skills) >= 250
    assert len(roadmaps) == len(careers)


def test_roadmaps_match_career_ids() -> None:
    career_ids = {career["id"] for career in load_json("careers.json")}

    assert set(load_json("roadmaps.json")) == career_ids
