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
