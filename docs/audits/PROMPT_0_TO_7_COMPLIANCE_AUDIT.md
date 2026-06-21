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

## Prompt 4 — Career Tools & Scoring Engine Audit

Status: PASS

- Cached career and skill loaders validate local JSON resources.
- Text/list normalization, alias matching, interest, skill, and goal scoring are implemented.
- Formula remains 35% interest, 45% skill, and 20% career-goal relevance.
- Dict and Pydantic profiles, top-k bounds, deterministic ranking, and non-mutation are tested.
- Recommendations include score breakdown, matched reasons/skills, missing skills, and safety note.
- The audit repeated the same profile and received identical results.

## Prompt 5 — Multi-Agent Workflow Audit

Status: PASS

- `SkillGapAgent` returns ordered matched, missing, priority skills, and bounded readiness.
- `RoadmapAgent` returns stored roadmaps and a schema-valid fallback.
- `CareerAdvisorAgent` orchestrates scoring, gap analysis, and roadmap retrieval.
- Dict and Pydantic inputs produce `AgentRecommendationResponse`-valid output.
- `POST /recommend` returned HTTP 200 for valid input and 422 for malformed input.
- Existing health, metadata, and validation endpoints remain compatible.

## Prompt 6 — MCP-Style Server Audit

Status: PASS

- Career listing, lookup, interest search, required skills, roadmap, and skill metadata tools work.
- Skill listing/search and the machine-readable tool catalog work.
- Pagination, filters, deterministic search ordering, and resource copying are covered by tests.
- All MCP endpoints in the smoke scope returned HTTP 200.
- Missing career and skill resources are covered by tests and return safe HTTP 404 responses.

## Prompt 7 — Agent Skill Audit

Status: PASS

- The Career Advisor Skill has all 18 required progressive-disclosure sections.
- It names the implemented schemas, agents, scoring workflow, and MCP-style tools.
- Safety, failure handling, examples, testing notes, boundaries, and future work are explicit.
- It does not claim employment guarantees or clinical diagnosis capabilities.
- `app/skills/README.md` and `tests/test_agent_skill_docs.py` exist.

## API Compatibility Audit

Status: PASS

- Compliance smoke checks: 10/10, including controlled 422 and 404 behavior.
- Standalone API smoke script: 9/9 critical endpoint requests returned HTTP 200.
- Existing endpoint response contracts remain unchanged by this audit.

## Test Coverage Audit

Status: PASS

- 13 focused test modules cover health, data, schemas, tools, agents, APIs, MCP, and skill docs.
- Pytest result: 122 passed, 0 failed.
- Tests are deterministic, offline, and require no API key.

## Security Hygiene Audit

Status: PASS

- No `.env`, cache directory, bytecode, dependency tree, or build output is tracked.
- The tracked-source scanner found no API key, GitHub token, private key, or assigned secret.
- `.env.example` contains empty placeholders only.
- Dataset scan found no guaranteed employment, job, salary, or accuracy claim.
- Recommendation responses contain the required educational safety notice.
- Controlled validation and missing-resource paths return safe 422/404 responses.

## Git Hygiene Audit

Status: PASS

- Audit started on `main` synchronized with `origin/main`.
- Changes were committed incrementally; generated caches remain ignored and untracked.
- Remote `origin` is configured for the expected public repository.
