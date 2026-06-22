# Operations Runbook

## Overview
This runbook guides operators through common troubleshooting workflows, incident response checks, monitoring indicators, and system checks for the CareerVerse Agent app.

## Service Health Checks
Verify if the API process is alive and responsive:
- **Endpoint**: `GET /api/v1/health/live`
- **Verification Command**:
  ```bash
  curl -sI http://127.0.0.1:8000/api/v1/health/live | grep "HTTP/1.1 200"
  ```
- **Action on failure**: Restart the container or the dev process. Check if Port 8000 is occupied.

## Readiness Checks
Verify if internal datasets are loaded and repositories are functional:
- **Endpoint**: `GET /api/v1/health/ready`
- **Action on failure**: Check application start logs. Ensure `careers.json`, `skills.json`, and `roadmaps.json` are present in `app/data/` and not corrupted.

## Common Failure Modes

### 1. Docker Troubleshooting
- **Symptom**: Container exits immediately upon starting.
- **Troubleshooting**: Check container start logs:
  ```bash
  docker logs careerverse-agent-api
  ```
  Verify if the environment variable `ENVIRONMENT` is set. Confirm port binding is correctly mapped.

### 2. API Troubleshooting
- **Symptom**: Endpoint `/api/v1/recommend` returns `400 Bad Request` or `500 Internal Error`.
- **Troubleshooting**:
  - Check the response header `X-Request-ID` and locate the matching request trace in the logs.
  - If error code is `400` with detail "Input safety violation detected", it indicates a rejected prompt injection.
  - If error code is `500`, inspect stack traces.

### 3. Frontend Troubleshooting
- **Symptom**: Dashboard fails to load or reports "API Connection Error".
- **Troubleshooting**:
  - Inspect browser console logs.
  - Verify that the backend is running.
  - Check that the `VITE_API_BASE_URL` environment variable is configured correctly.

### 4. Evaluation Troubleshooting
- **Symptom**: `evaluate_agent` reports failures.
- **Troubleshooting**:
  - Run python scripts `python scripts/validate_domain_dataset.py` to confirm mock dataset fields have not been modified.

## Security Incident Checklist
If a potential secret leak, breach, or injection flood is reported:
1. **Redact logs**: Never copy or upload logs containing system credentials or API tokens.
2. **Review inputs**: Check transaction logs for rejected injection payloads.
3. **Secret Revocation**: If a real `GOOGLE_API_KEY` is leaked, revoke it immediately inside GCP Secret Manager.
4. **Isolate**: Temporarily suspend external endpoints if anomalous traffic is detected.

## Rollback Procedure
If the deployed release causes major operational issues:
1. **Locate active revision**: Identify the previous stable image tag (e.g. `gcr.io/YOUR_PROJECT_ID/careerverse-agent-api:vX.Y.Z`).
2. **Redeploy**: Redeploy pointing to that revision to restore operations immediately.
3. **Verify**: Call `/api/v1/health/live` to ensure the rollback was successful.

## Log Review Guidelines
- Look for `X-Request-ID` tracing tags to follow execution steps.
- Do not print request bodies, passwords, or emails.
- Check duration metrics in completed transaction logs:
  `HTTP POST /api/v1/recommend -> 200 (215.42 ms)`

## Release Checklist
Before tagging any new release tag:
1. Run local pre-deploy verification:
   ```bash
   python scripts/pre_deploy_check.py
   ```
2. Confirm `ruff check` reports no lint errors.
3. Confirm `pytest` returns zero failures.
4. Verify `git status` shows no untracked `.env` files.
