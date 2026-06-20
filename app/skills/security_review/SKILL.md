---
name: security-review
description: Review CareerVerse Agent changes for secret safety, input validation, prompt injection defense, responsible AI, and public demo readiness. Use for environment variables, API responses, user input, prompt handling, agent behavior, public documentation, or GitHub submission work.
---

# Security Review Skill

## Purpose

Review CareerVerse Agent changes for security, responsible AI, and public demo safety.

## When to Use

Use this skill whenever changes involve:

- Environment variables
- API responses
- User input
- Prompt handling
- Agent behavior
- Public documentation
- GitHub-ready submission

## Security Checklist

Verify:

- No `.env` file is committed.
- No API keys are committed.
- No passwords or tokens are committed.
- No private user data is included.
- `.env.example` contains placeholders only.
- User input is validated.
- Prompt injection attempts are handled safely.
- Error messages do not leak internals.
- Logs do not expose secrets.
- AI outputs include educational guidance disclaimers.

## Responsible AI Checklist

The system must not:

- Guarantee employment.
- Claim psychological diagnosis.
- Replace professional counseling.
- Ask for unnecessary sensitive data.
- Present recommendations as absolute truth.

## Output

Report:

- Security checks performed
- Files inspected
- Issues fixed
- Any remaining risk
