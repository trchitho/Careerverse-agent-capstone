# Prompt 9 Local Evaluation Pipeline Audit

## Summary

The Prompt 8 security audit was confirmed as `PASS` before implementation. Prompt 9 adds a
deterministic offline evaluation pipeline that exercises recommendation quality signals, response
contracts, skill gaps, roadmaps, safety blocking, normalization, Vietnamese input, and invalid
profiles without network access, external APIs, databases, randomness, or API keys.

## Files Changed

- `app/evals/test_cases.json`
- `app/evals/evaluation_schema.py`
- `app/evals/evaluate_agent.py`
- `tests/test_agent_workflow.py`
- `tests/test_safety.py`
- `tests/test_evaluation_pipeline.py`
- README, metadata stage, and audit fixture allowlist

## Evaluation Cases

The suite contains 14 synthetic cases:

- 7 normal role-oriented profiles
- 4 edge profiles
- 1 prompt-injection security profile
- 2 invalid profiles

Coverage includes AI full-stack, backend, data, frontend, cloud/DevOps, product, security,
career changing, beginner roadmaps, Vietnamese goals, and duplicate normalization.

## Evaluation Script

Run with:

```text
python -m app.evals.evaluate_agent
```

The runner validates case schemas, dispatches success/security/invalid paths, validates the
`AgentRecommendationResponse`, checks bounded scores, roadmap lengths, safety notice, expected
career keywords, and missing-skill signals. It prints each result, calculates a percentage, and
returns exit code 1 if any required case fails.

## Test Coverage

- `tests/test_agent_workflow.py`: agent, response schema, determinism, API, and MCP compatibility.
- `tests/test_safety.py`: integration-level blocking, non-echo, redaction, and invalid input.
- `tests/test_evaluation_pipeline.py`: case contracts, coverage, aggregate result, and CLI execution.

## Security Cases

The security case confirms a high-risk prompt injection is blocked without echoing malicious
source text. Existing Prompt 8 safety tests remain active and passing.

## Commands Run

```text
python scripts/validate_domain_dataset.py
python scripts/audit_prompt_0_to_7.py
python scripts/smoke_test_api.py
python -m app.evals.evaluate_agent
python -m compileall app
ruff check .
pytest -q
python -m app.evals.validate_domain_data
```

## Results

- Domain dataset validation: PASS, 80 careers, 260 skills, 80 roadmaps.
- Prompt 0–7 audit: PASS, 35/35 checks.
- API smoke test: PASS, 9/9 endpoints.
- Local evaluation: PASS, 14/14 cases, score 100.00%.
- Compile: PASS.
- Ruff: PASS.
- Pytest: 180 passed, 0 failed.
- Compatibility domain validator: PASS.

## Remaining Risks

- Keyword expectations validate broad role relevance, not semantic career-advice quality.
- The curated 14-case suite does not represent every learner background or language variation.
- Dataset or scoring changes may require intentional expectation review rather than blind updates.
- Prompt 10 should document evaluation limitations and separate measured behavior from future work.
- Future evaluation can add larger regression sets, fairness slices, and tracked quality metrics.

These are transparent limitations, not failures of the deterministic Prompt 9 scope.

## Final Verdict

PASS
