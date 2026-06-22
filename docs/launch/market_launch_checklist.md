# Market Launch Checklist

This checklist tracks go-live requirements to verify the CareerVerse Agent is stable, secure, and compliant.

## Product Readiness
- [ ] Career recommendations verified against all 14 student test profiles.
- [ ] Roadmap synthesis returns correctly formatted 30-day and 8-week plans.
- [ ] UI Dashboard displays career recommendations, skill gap metrics, roadmaps, and disclaimers.

## Technical Readiness
- [ ] Python backend compiles without syntax errors.
- [ ] React frontend compiles and builds successfully (`npm run build`).
- [ ] Pre-deployment verification script passes locally (`python scripts/pre_deploy_check.py`).
- [ ] Unit test coverage verified via pytest (220+ tests pass).
- [ ] Docker container starts and passes local API checks.

## Safety Readiness
- [ ] Prompt injection safety gates block instruction overrides and returns 400 Bad Request.
- [ ] Security scanners verify that no real secrets or API keys are committed.
- [ ] Verification script asserts no `.env` files are tracked in the Git index.
- [ ] Clinical and psychological diagnosis disclaimer is clearly displayed in responses.
- [ ] Job outcome/employment guarantee disclaimer is present in the UI and README.

## Documentation Readiness
- [ ] README is updated with Web UI, Observability, CI/CD, and Launch Pack details.
- [ ] Architecture design details mapped out in `docs/architecture.md`.
- [ ] All API endpoints documented with copy-pasteable examples in `docs/api_examples.md`.
- [ ] Operations Runbook and Deployment guides completed.

## Demo Readiness
- [ ] Demo script in `docs/demo_script.md` is aligned with current API and Web UI layouts.
- [ ] Mock profile configurations prepared for clean, repeatable walkthroughs.

## Deployment Readiness
- [ ] Primary deployment destination Google Cloud Run instructions prepared.
- [ ] Alternative hosting routes (Railway, Render, Fly.io) documented.
- [ ] Production environment variables are mapped without hardcoding secrets.

## Feedback Readiness
- [ ] Feedback Solicitation endpoint returns correct status codes.
- [ ] Feedback comments undergo input safety filtration.
- [ ] Ephemeral storage behavior (InMemory) is clearly documented.

## Legal and Privacy Review
- [ ] Student data collection follows data minimization standards.
- [ ] No email, phone number, or address collection is requested in the feedback form.
- [ ] Privacy guidelines clearly specify that feedback storage is for demo purposes only.

## Final Go / No-Go
- [ ] Final readiness verdict is set to PASS.
