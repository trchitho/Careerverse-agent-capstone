"""MCP-style local career resource server for the Kaggle Capstone."""

from copy import deepcopy
from typing import Any

from app.agents import RoadmapAgent
from app.tools.career_tools import (
    build_search_text,
    load_careers,
    load_skills,
    normalize_text,
    tokenize_text,
)

MAX_PAGE_SIZE = 100


def _validate_pagination(limit: int, offset: int) -> None:
    """Validate shared pagination bounds."""
    if not 1 <= limit <= MAX_PAGE_SIZE:
        raise ValueError("limit must be between 1 and 100")
    if offset < 0:
        raise ValueError("offset must be greater than or equal to 0")


def _paginate(items: list[dict[str, Any]], limit: int, offset: int) -> dict[str, Any]:
    """Return a copied, stable paginated resource response."""
    _validate_pagination(limit, offset)
    page = deepcopy(items[offset : offset + limit])
    return {
        "items": page,
        "count": len(page),
        "total": len(items),
        "limit": limit,
        "offset": offset,
    }


class CareerMCPServer:
    """Expose local career knowledge as machine-readable tool resources."""

    def __init__(self, roadmap_agent: RoadmapAgent | None = None) -> None:
        self.roadmap_agent = roadmap_agent or RoadmapAgent()

    @staticmethod
    def _career_summary(career: dict[str, Any]) -> dict[str, Any]:
        """Return the lightweight career listing representation."""
        return {
            "career_id": career["id"],
            "title": career["title"],
            "family": career.get("family"),
            "level": career.get("level"),
            "description": career["description"],
            "market_relevance": deepcopy(career.get("market_relevance")),
        }

    @staticmethod
    def _matches_filter(value: object, expected: str | None) -> bool:
        """Apply an optional case-insensitive exact filter."""
        if expected is None:
            return True
        normalized = normalize_text(expected)
        if not normalized:
            raise ValueError("filter values must not be blank")
        return normalize_text(str(value or "")) == normalized

    def list_available_careers(
        self,
        family: str | None = None,
        level: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List lightweight career resources with optional filters."""
        filtered = [
            self._career_summary(career)
            for career in load_careers()
            if self._matches_filter(career.get("family"), family)
            and self._matches_filter(career.get("level"), level)
        ]
        filtered.sort(
            key=lambda item: (
                normalize_text(str(item["title"])),
                normalize_text(str(item["career_id"])),
            )
        )
        return _paginate(filtered, limit, offset)

    def get_career_by_id(self, career_id: str) -> dict[str, Any]:
        """Return one full career resource by normalized identifier."""
        normalized = normalize_text(career_id)
        if not normalized:
            raise ValueError("career_id must not be blank")
        for career in load_careers():
            if normalize_text(str(career["id"])) == normalized:
                return deepcopy(career)
        raise ValueError(f"Career not found: {career_id}")

    @staticmethod
    def _career_search_score(query: str, career: dict[str, Any]) -> float:
        """Calculate deterministic token and phrase relevance."""
        query_normalized = normalize_text(query)
        query_tokens = tokenize_text(query)
        search_text = build_search_text(career)
        search_tokens = tokenize_text(search_text)
        score = len(query_tokens & search_tokens) * 10.0
        if query_normalized == normalize_text(str(career.get("title", ""))):
            score += 100.0
        elif query_normalized in normalize_text(str(career.get("title", ""))):
            score += 50.0
        if query_normalized in search_text:
            score += 20.0
        return score

    def search_careers_by_interest(
        self,
        interest: str,
        limit: int = 10,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search career resources by interest and contextual career text."""
        query = normalize_text(interest)
        if not query:
            raise ValueError("interest must not be blank")
        scored = [
            (self._career_search_score(query, career), career)
            for career in load_careers()
        ]
        matches = [(score, career) for score, career in scored if score > 0]
        matches.sort(
            key=lambda item: (
                -item[0],
                normalize_text(str(item[1]["title"])),
                normalize_text(str(item[1]["id"])),
            )
        )
        items = [self._career_summary(career) for _score, career in matches]
        response = _paginate(items, limit, offset)
        response["query"] = interest.strip()
        return response

    @staticmethod
    def _skill_lookup_index() -> dict[str, dict[str, Any]]:
        """Build normalized id, name, and alias lookups."""
        index: dict[str, dict[str, Any]] = {}
        for skill in load_skills():
            candidates = [skill.get("id"), skill.get("name"), *skill.get("aliases", [])]
            for candidate in candidates:
                normalized = normalize_text(str(candidate or ""))
                if normalized:
                    index.setdefault(normalized, skill)
        return index

    def get_skill_metadata(self, skill_name: str) -> dict[str, Any]:
        """Return one skill resource by id, name, or alias."""
        normalized = normalize_text(skill_name)
        if not normalized:
            raise ValueError("skill_name must not be blank")
        skill = self._skill_lookup_index().get(normalized)
        if skill is None:
            raise ValueError(f"Skill not found: {skill_name}")
        return deepcopy(skill)

    def get_required_skills(self, career_id: str) -> dict[str, Any]:
        """Return career skill requirements enriched with metadata."""
        career = self.get_career_by_id(career_id)
        index = self._skill_lookup_index()

        def enrich(names: list[str]) -> list[dict[str, Any]]:
            return [
                {
                    "name": name,
                    "metadata": deepcopy(index.get(normalize_text(name))),
                }
                for name in names
            ]

        return {
            "career_id": career["id"],
            "title": career["title"],
            "required_skills": enrich(career.get("required_skills", [])),
            "nice_to_have_skills": enrich(career.get("nice_to_have_skills", [])),
        }

    def get_roadmap_for_career(self, career_id: str) -> dict[str, Any]:
        """Return a stored roadmap resource without generating a fallback."""
        normalized = normalize_text(career_id)
        if not normalized:
            raise ValueError("career_id must not be blank")
        for key, roadmap in self.roadmap_agent.load_roadmaps().items():
            if normalize_text(key) == normalized:
                return deepcopy(roadmap)
        raise ValueError(f"Roadmap not found for career: {career_id}")

    def list_available_skills(
        self,
        category: str | None = None,
        level: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List skill resources with optional exact filters."""
        filtered = [
            deepcopy(skill)
            for skill in load_skills()
            if self._matches_filter(skill.get("category"), category)
            and self._matches_filter(skill.get("level"), level)
        ]
        filtered.sort(
            key=lambda skill: (
                normalize_text(str(skill["name"])),
                normalize_text(str(skill["id"])),
            )
        )
        return _paginate(filtered, limit, offset)

    @staticmethod
    def _skill_search_score(query: str, skill: dict[str, Any]) -> float:
        """Calculate deterministic skill search relevance."""
        query_tokens = tokenize_text(query)
        fields = [
            skill.get("id", ""),
            skill.get("name", ""),
            skill.get("description", ""),
            *skill.get("aliases", []),
            *skill.get("related_skills", []),
        ]
        search_text = normalize_text(" ".join(str(field) for field in fields))
        score = len(query_tokens & tokenize_text(search_text)) * 10.0
        if query == normalize_text(str(skill.get("name", ""))):
            score += 100.0
        elif query in search_text:
            score += 20.0
        return score

    def search_skills(
        self,
        query: str,
        category: str | None = None,
        level: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search skill resources with optional category and level filters."""
        normalized = normalize_text(query)
        if not normalized:
            raise ValueError("query must not be blank")
        scored = [
            (self._skill_search_score(normalized, skill), skill)
            for skill in load_skills()
            if self._matches_filter(skill.get("category"), category)
            and self._matches_filter(skill.get("level"), level)
        ]
        matches = [(score, skill) for score, skill in scored if score > 0]
        matches.sort(
            key=lambda item: (
                -item[0],
                normalize_text(str(item[1]["name"])),
                normalize_text(str(item[1]["id"])),
            )
        )
        response = _paginate([skill for _score, skill in matches], limit, offset)
        response["query"] = query.strip()
        return response
