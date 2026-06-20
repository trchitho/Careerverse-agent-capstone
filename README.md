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

## Development

```bash
python -m compileall app
ruff check .
pytest
```
