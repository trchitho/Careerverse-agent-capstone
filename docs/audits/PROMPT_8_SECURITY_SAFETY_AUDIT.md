# Prompt 8 Security & Responsible AI Audit

## Summary

The Prompt 0–7 compliance audit was confirmed as `PASS` before implementation. Prompt 8 adds a
deterministic, offline safety boundary that detects explicit prompt injection, redacts supported
sensitive data, blocks severe disclosures, and preserves the educational safety notice.

## Files Changed

- `app/tools/safety_tools.py` and `app/tools/__init__.py`
- `app/main.py` and `app/agents/career_advisor_agent.py`
- `app/evals/security_test_cases.json`
- security tool, API, and repository hygiene tests
- README, architecture, and Career Advisor Skill documentation

## Safety Tools Implemented

- `detect_prompt_injection()`
- `validate_profile_safety()`
- `redact_sensitive_text()`
- `get_safety_notice()`

Detection covers instruction override, system/developer prompt extraction, secret extraction,
security bypass, guardrail disabling, and jailbreak phrases. Redaction covers emails, assigned
passwords/tokens, private keys, supported provider token formats, and long numeric identifiers.

## API Integration

`POST /recommend` validates the normalized profile before calling `CareerAdvisorAgent`.

- Unsafe injection or severe secret exposure returns HTTP 400 with a stable `unsafe_profile`
  error, risk level, and generic message.
- The response does not include matched phrases, source secrets, or malicious profile text.
- Lower-risk identifiers such as emails are redacted before agent orchestration.
- Successful responses use the exact canonical educational safety notice.
- Existing validation, health, metadata, tool catalog, and MCP routes remain available.

## Tests Added

- `tests/test_safety_tools.py`
- `tests/test_recommend_safety_api.py`
- `tests/test_security_hygiene.py`

Existing recommendation and metadata tests were updated for the new safety boundary and stage.

## Validation Commands

```text
python scripts/validate_domain_dataset.py
python scripts/audit_prompt_0_to_7.py
python scripts/smoke_test_api.py
python -m compileall app
ruff check .
pytest -q
python -m app.evals.validate_domain_data
python <skill-creator>/scripts/quick_validate.py app/skills/career_advisor
```

## Results

- Prompt 0–7 compliance audit: PASS, 35/35 checks.
- Domain dataset validation: PASS, 80 careers, 260 skills, 80 roadmaps.
- API smoke test: PASS, 9/9 endpoints.
- Python compile: PASS.
- Ruff: PASS.
- Pytest: 159 passed, 0 failed.
- Compatibility domain validator: PASS.
- Career Advisor Skill validation: PASS.

## Remaining Risks

- Pattern-based detection is intentionally conservative and is not a semantic moderation model.
- Unicode confusables, fragmented adversarial phrases, and novel injection wording may evade a
  fixed phrase list.
- Redaction is limited to supported public-demo formats and is not a full data-loss-prevention
  system.
- Production deployment would still require trusted proxy controls, rate limiting, structured
  redacted logging, monitoring, and incident response.
- Prompt 9 should measure false positives, false negatives, and safety regression cases locally.

These risks are documented limitations rather than failures of the offline Prompt 8 scope.

## Final Verdict

PASS
