# Architecture

CareerVerse Agent follows a modular FastAPI backend structure.

The detailed architecture will be expanded in later implementation prompts.

## MCP-Style Career Data Server

The MCP-style server exposes the local career knowledge base as machine-readable resources.
Agents can retrieve career profiles, required skills, skill metadata, and stored roadmap
templates through deterministic local tools without external APIs.

## Agent Skill Layer

The Career Advisor Skill documents how to execute the workflow safely and consistently. It
provides a reusable instruction layer for future agent implementations, evaluations, and demos.

## Safety Layer

Before recommendation orchestration, the API validates normalized profile text through a
deterministic safety layer. Explicit instruction overrides and severe secret exposure are blocked
without echoing source text. Lower-risk personal identifiers are redacted before the agent runs,
and every successful recommendation includes the canonical educational safety notice.
