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
