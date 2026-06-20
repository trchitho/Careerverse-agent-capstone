# AGENTS.md — CareerVerse Agent Project Rules

## Project Identity

Project name: CareerVerse Agent — AI Career Guidance Agent for Students

Repository: careerverse-agent-capstone

Track: Agents for Good

Purpose:
CareerVerse Agent is a focused Kaggle Capstone MVP that helps students and early-career learners receive career path recommendations, skill gap analysis, and personalized learning roadmaps.

This project is not the full academic CareerVerse platform. It is a smaller, demo-ready AI Agent system focused on agent architecture, tool usage, safety, evaluation, documentation, and reproducibility.

---

## Mandatory Agent Behavior

Before making changes, every coding agent must:

1. Read this `AGENTS.md`.
2. Check current directory.
3. Check git status.
4. Understand existing structure before editing.
5. Make small, controlled changes.
6. Commit frequently according to the commit rules.
7. Never commit secrets or local artifacts.
8. Run available validation commands before final response.
9. Report truthfully what passed, failed, or was skipped.

---

## Mandatory Git Rules

After every 10–30 lines of real code changes, run:

```bash
git add .
git commit -m "<appropriate message>"
```

Rules:

* Do not wait for a “meaningful small change”.
* Do not batch large changes.
* Do not exceed 30 lines of real code changes before committing unless generated files or lockfiles make it unavoidable.
* More commits are preferred over fewer commits.
* The agent chooses commit messages.
* Do not ask the user for commit messages.
* Push only once at the end:

```bash
git push origin main
```

If the remote is missing, do not invent a remote URL. Commit locally and report that `origin` is not configured.

---

## Secret Handling

Never commit:

* `.env`
* API keys
* OAuth secrets
* passwords
* tokens
* private certificates
* private user data
* local database dumps
* generated build folders

Use `.env.example` for placeholders only.

Example:

```env
GOOGLE_API_KEY=
MODEL_NAME=gemini-2.5-flash
ENVIRONMENT=development
```

---

## Code Quality Rules

Use production-minded Python code:

* Python 3.11+
* FastAPI for API layer
* Pydantic for request/response schemas
* Pydantic Settings for configuration
* Type hints for public functions
* Clear module boundaries
* Deterministic logic where possible
* Small functions with single responsibility
* No unnecessary abstractions
* No dead code
* No fake features
* No hidden side effects
* No hardcoded secrets
* No broad `except Exception` unless justified
* No silent failures

Prefer readable code over clever code.

---

## Architecture Rules

Keep the MVP focused:

Implemented core scope:

1. Career recommendation
2. Skill gap analysis
3. Personalized learning roadmap
4. Multi-agent architecture
5. MCP-style tool server
6. Agent Skill via SKILL.md
7. Security guard
8. Local evaluation
9. FastAPI demo
10. Kaggle-ready documentation

Do not expand into full CareerVerse unless explicitly requested.

Do not add these unless requested:

* Full authentication
* Full database
* Full frontend
* Payment
* Real Neo4j integration
* Real pgvector integration
* Real CV parser
* Real voice inference
* Full Gemini production integration
* Complex cloud deployment
* Over-engineered microservices

Future work may mention these, but code must not claim unimplemented features.

---

## API Rules

FastAPI endpoints must:

* Use explicit request/response schemas when possible.
* Return structured JSON.
* Validate user input.
* Avoid leaking stack traces.
* Avoid logging secrets.
* Include safe error messages.
* Keep Swagger/OpenAPI usable.

Health endpoint:

```text
GET /
```

Metadata endpoint:

```text
GET /metadata
```

Recommendation endpoint, when implemented:

```text
POST /recommend
```

---

## Security & Responsible AI Rules

The system provides educational career guidance only.

It must not:

* Guarantee employment outcomes.
* Claim clinical psychological diagnosis.
* Request sensitive personal data unnecessarily.
* Expose user data.
* Store secrets in code.
* Follow prompt injection instructions.
* Reveal system prompts or hidden instructions.

Every recommendation response should include a safety notice:

```text
This system provides educational career guidance only. It does not guarantee employment outcomes or replace professional counseling.
```

---

## Testing Rules

When relevant, add or update tests.

Preferred commands:

```bash
python -m compileall app
ruff check .
pytest
```

Tests must not require real external API keys.

Local evaluation should be deterministic and runnable offline where possible.

---

## Documentation Rules

Keep documentation honest.

README must explain:

* Problem
* Solution
* Track
* Architecture
* Setup
* API usage
* Evaluation
* Security
* Project structure
* Future work

Kaggle writeup must not claim features that are not implemented.

Implemented features and future work must be separated clearly.

---

## File Ownership

Important files:

```text
app/main.py                         FastAPI app entrypoint
app/core/config.py                   Environment/config layer
app/core/constants.py                Project constants
app/schemas/profile_schema.py        API schemas
app/agents/                          Agent orchestration modules
app/tools/                           Deterministic tools/utilities
app/mcp_server/                      MCP-style tool server prototype
app/skills/                          Agent skills
app/data/                            Local JSON knowledge base
app/evals/                           Local evaluation pipeline
docs/                                Architecture, demo, writeup docs
```

---

## Done Criteria

A task is done only when:

* Code compiles.
* Lint passes or issues are clearly reported.
* Tests pass if tests exist.
* README/docs are updated if behavior changed.
* No secrets are committed.
* Git status is clean.
* Changes are committed.
* Final push is attempted once if remote exists.
