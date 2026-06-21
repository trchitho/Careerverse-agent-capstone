# CareerVerse Agent

CareerVerse Agent — AI Career Guidance Agent for Students.

## Track

Agents for Good

## Problem

Students and early-career learners often struggle to translate their interests, current skills,
and goals into a clear career direction.

## Solution

CareerVerse Agent is a focused AI agent MVP that will recommend career paths, analyze skill
gaps, and generate personalized learning roadmaps.

## Current Scope

This initial version bootstraps the backend architecture for the Kaggle Capstone project.

## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic
- Pydantic Settings
- pytest
- ruff

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` only for local configuration. The API key is optional during
bootstrap and must never be committed.

## API

```text
GET /
GET /metadata
POST /profiles/validate
POST /recommend
```

Interactive API documentation is available at `/docs` while the server is running.

## Input Validation

The API uses Pydantic v2 schemas to validate and normalize user profile input.

Current validation endpoint:

```text
POST /profiles/validate
```

It checks:

- required profile fields
- non-empty interests and skills
- duplicate normalization
- supported language values
- supported learning styles and experience levels
- basic prompt-injection patterns
- safe public-demo input constraints

## Career Scoring Engine

The project uses a deterministic, explainable scoring engine before adding full agent
orchestration.

The current score combines:

- Interest match: 35%
- Skill match: 45%
- Career goal relevance: 20%

The engine returns ranked recommendations, score breakdowns, matched reasons, matched skills,
missing skills previews, and an educational safety note.

## Multi-Agent Workflow

The backend includes a deterministic multi-agent workflow:

1. `CareerAdvisorAgent` orchestrates the recommendation flow.
2. `SkillGapAgent` compares user skills with target career requirements.
3. `RoadmapAgent` retrieves a matching 30-day and 8-week roadmap.

Main endpoint:

```text
POST /recommend
```

The response includes top recommendations, score breakdowns, skill gap analysis, a personalized
roadmap, and an educational safety notice.

## MCP-Style Tool Server

The project exposes local career, skill, and roadmap datasets through MCP-style tool endpoints.

```text
GET /tools
GET /mcp/careers
GET /mcp/careers/{career_id}
GET /mcp/careers/{career_id}/skills
GET /mcp/careers/{career_id}/roadmap
GET /mcp/skills
GET /mcp/skills/{skill_name}
GET /mcp/search/careers?q=AI
GET /mcp/search/skills?q=Python
```

This is a local MCP-style prototype for the Kaggle Capstone. It requires no external APIs,
secrets, or production database.

## Agent Skills

This project documents agent behavior through reusable skill files.

Main skill:

```text
app/skills/career_advisor/SKILL.md
```

The Career Advisor Skill defines usage conditions, inputs, validation, multi-agent workflow,
MCP-style tools, output contracts, safety rules, failure handling, and examples.

Supporting skills:

```text
app/skills/code_quality/SKILL.md
app/skills/security_review/SKILL.md
app/skills/kaggle_submission/SKILL.md
```

```bash
pytest tests/test_career_tools.py
```

## Domain Data

This project uses production-minded local JSON datasets for a reproducible Kaggle Capstone demo:

- `app/data/careers.json`: career profiles, required skills, daily work, market relevance,
  and fit explanations
- `app/data/skills.json`: skill catalog with categories, levels, aliases, related skills,
  and assessment hints
- `app/data/roadmaps.json`: 30-day and 8-week learning roadmaps for every career profile

The dataset is generated and validated locally without external APIs, secrets, or private data.

```bash
python scripts/generate_domain_dataset.py
python scripts/validate_domain_dataset.py
```

## Development

```bash
python -m compileall app
python -m app.evals.validate_domain_data
ruff check .
pytest
```

## Security

Do not commit `.env`, API keys, passwords, tokens, build output, or local cache files.

CareerVerse Agent provides educational guidance only and does not guarantee employment
outcomes or replace professional counseling.

## Kaggle Capstone Concepts

- Agent / Multi-agent system
- MCP-style tool integration
- Agent Skills
- Security and input validation
- Local evaluation pipeline
- FastAPI deployability

## Project Rules

This repository uses `AGENTS.md` as the global instruction file for coding agents.

Before making changes, read:

- `AGENTS.md`
- `docs/PROJECT_RULES.md`
- `docs/CODE_QUALITY_RULES.md`
- `docs/SECURITY_RULES.md`
- `docs/GIT_WORKFLOW_RULES.md`

Future implementation prompts should follow these rules without repeating them.
