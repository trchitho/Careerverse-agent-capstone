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
