"""Tests for MCP-style local career resource tools."""

from copy import deepcopy

import pytest

from app.mcp_server import CareerMCPServer


@pytest.fixture
def server() -> CareerMCPServer:
    return CareerMCPServer()


def test_list_available_careers_is_paginated(
    server: CareerMCPServer,
) -> None:
    response = server.list_available_careers(limit=5, offset=2)

    assert response["count"] == 5
    assert response["limit"] == 5
    assert response["offset"] == 2
    assert response["total"] >= 80


def test_career_listing_filters_by_family(
    server: CareerMCPServer,
) -> None:
    first = server.list_available_careers(limit=1)["items"][0]
    family = server.get_career_by_id(first["career_id"])["family"]

    response = server.list_available_careers(family=family, limit=100)

    assert response["items"]
    assert all(item["family"] == family for item in response["items"])


def test_get_career_by_id_returns_full_resource(
    server: CareerMCPServer,
) -> None:
    career_id = server.list_available_careers(limit=1)["items"][0]["career_id"]

    career = server.get_career_by_id(career_id)

    assert career["id"] == career_id
    assert career["required_skills"]
    assert career["recommended_for"]


def test_get_career_by_id_rejects_unknown_resource(
    server: CareerMCPServer,
) -> None:
    with pytest.raises(ValueError, match="Career not found"):
        server.get_career_by_id("not_real_id")


def test_search_careers_returns_ranked_matches(
    server: CareerMCPServer,
) -> None:
    response = server.search_careers_by_interest("AI", limit=5)

    assert response["query"] == "AI"
    assert response["items"]
    assert response["count"] <= 5


def test_search_careers_rejects_blank_query(
    server: CareerMCPServer,
) -> None:
    with pytest.raises(ValueError, match="interest"):
        server.search_careers_by_interest("   ")


def test_get_required_skills_includes_metadata(
    server: CareerMCPServer,
) -> None:
    career_id = server.list_available_careers(limit=1)["items"][0]["career_id"]

    response = server.get_required_skills(career_id)

    assert response["required_skills"]
    assert response["nice_to_have_skills"]
    assert response["required_skills"][0]["metadata"] is not None


def test_get_roadmap_for_career_returns_stored_resource(
    server: CareerMCPServer,
) -> None:
    career_id = server.list_available_careers(limit=1)["items"][0]["career_id"]

    roadmap = server.get_roadmap_for_career(career_id)

    assert roadmap["career_id"] == career_id
    assert len(roadmap["thirty_day_plan"]) == 4
    assert len(roadmap["eight_week_plan"]) == 8


def test_get_roadmap_rejects_unknown_career(
    server: CareerMCPServer,
) -> None:
    with pytest.raises(ValueError, match="Roadmap not found"):
        server.get_roadmap_for_career("not_real_id")


def test_get_skill_metadata_by_name_id_and_alias(
    server: CareerMCPServer,
) -> None:
    skill = server.list_available_skills(limit=1)["items"][0]

    assert server.get_skill_metadata(skill["name"])["id"] == skill["id"]
    assert server.get_skill_metadata(skill["id"])["name"] == skill["name"]
    if skill.get("aliases"):
        assert server.get_skill_metadata(skill["aliases"][0])["id"] == skill["id"]


def test_get_skill_metadata_rejects_unknown_skill(
    server: CareerMCPServer,
) -> None:
    with pytest.raises(ValueError, match="Skill not found"):
        server.get_skill_metadata("not_real_skill")


def test_list_and_search_skills(
    server: CareerMCPServer,
) -> None:
    listing = server.list_available_skills(limit=5)
    search = server.search_skills("Python", limit=5)

    assert listing["count"] == 5
    assert search["items"]
    assert any(item["name"] == "Python" for item in search["items"])
