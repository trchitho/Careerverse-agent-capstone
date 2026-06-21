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
