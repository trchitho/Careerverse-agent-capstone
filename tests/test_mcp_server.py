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
