# Prompt 0–7 Compliance Audit

## Audit Date

June 21, 2026

## Project Context

- Project: CareerVerse Agent — AI Career Guidance Agent for Students
- Track: Agents for Good
- Scope: Prompt 0 through Prompt 7 only
- Method: deterministic offline scripts, FastAPI TestClient, Ruff, compileall, and pytest

## Executive Summary

All required Prompt 0–7 implementation layers were found and verified. The production dataset,
schemas, deterministic scoring engine, multi-agent workflow, MCP-style tools, API routes, and
Agent Skill documentation are mutually compatible.

The audit added reusable compliance and API smoke scripts. Initial failures were isolated to
direct script import paths, scanner self-detection, and one Ruff line-length issue; all were fixed
without changing business logic.

Final automated result: 35/35 compliance checks passed, 9/9 API smoke checks passed, and
122/122 pytest tests passed.

## Verification Commands Run

```text
python scripts/validate_domain_dataset.py
python scripts/audit_prompt_0_to_7.py
python scripts/smoke_test_api.py
python -m compileall app
ruff check .
pytest -q
python -m app.evals.validate_domain_data
```

All commands completed successfully.

## Prompt 0 — Global Rules Audit

Status: PASS

- `AGENTS.md` and all four rule documents exist.
- Code quality, security review, and Kaggle submission skill files exist.
- Commit frequency, secret handling, validation commands, and documentation honesty are explicit.

## Prompt 1 — Bootstrap & Architecture Audit

Status: PASS

- FastAPI entrypoint, configuration, constants, requirements, and project configuration exist.
- `.env.example` contains placeholders only; `.gitignore` covers secrets, caches, and builds.
- `GET /` and `GET /metadata` returned HTTP 200 through TestClient.
- Application imports and OpenAPI-compatible metadata are available.

## Prompt 2 / 2.1 — Domain Dataset Audit

Status: PASS

- Careers: 80 records, 6,242 formatted lines.
- Skills: 260 records, 8,027 formatted lines.
- Roadmaps: 80 records, 21,122 formatted lines.
- Total domain data: 35,391 lines.
- Career ids/titles and skill ids/names are unique.
- Every career has exactly one roadmap and no extra roadmap key exists.
- Required object fields and responsible-claim constraints passed.
- Both production and compatibility dataset validators passed.

## Prompt 3 — Schemas & Input Validation Audit

Status: PASS

- Pydantic v2 profile and domain schemas exist with strict extra-field handling.
- Profile normalization, deduplication, enum bounds, list bounds, and injection checks are tested.
- `UserProfileSummary`, recommendation, skill gap, roadmap, and full response schemas exist.
- `POST /profiles/validate` returned HTTP 200 for valid input and validation tests cover 422 paths.
- Contract tests validate generated career, skill, and roadmap records.
