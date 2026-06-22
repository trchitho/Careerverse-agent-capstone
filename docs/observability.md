# Observability

## Overview
The CareerVerse Agent backend incorporates local observability layers to log system behavior, trace requests end-to-end, monitor health states, and gauge feedback loops without sacrificing user data privacy.

## Request ID Middleware
To enable distributed tracing and request auditing, a custom `RequestIdMiddleware` is registered in `app/middleware/request_id.py`:
- **Trace Injection**: Every HTTP request is assigned a unique UUID `X-Request-ID` header.
- **Request Headers**: If the client provides a safe, short `X-Request-ID` in the request header, it is reused to trace across systems.
- **Response Headers**: The same `X-Request-ID` is returned to the client in the response headers.
- **Auditing Logs**: Every completed request details the method, path, status code, processing duration in milliseconds, and the active `request_id`.

## Safe Logging Rules
The logger is initialized in `app/core/logging_config.py` using standard structured logs:
- **No Request Bodies**: Unvalidated raw user inputs and request payloads are never written to disk to protect client confidentiality.
- **No Secrets**: Standard hygiene rules run checks to prevent printing `.env` details or API tokens.
- **No Unsafe Path Logs**: Only generic API route paths are tracked; query strings that might hold private identifiers are sanitized.

## Live Health Check
Determines if the backend process is running:
- **Endpoint**: `GET /api/v1/health/live`
- **Response**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-06-22T08:45:00Z"
  }
  ```

## Readiness Check
Verifies if the agent system is ready to receive traffic (validates dataset loading and local directories):
- **Endpoint**: `GET /api/v1/health/ready`
- **Checks**:
  - Verifies that domain datasets are loaded and parsed.
  - Verifies the availability of repositories.
- **Response**:
  ```json
  {
    "status": "ready",
    "timestamp": "2026-06-22T08:45:00Z",
    "dataset_loaded": true
  }
  ```

## Metrics Summary
Provides aggregated feedback statistics and deployment status flags:
- **Endpoint**: `GET /api/v1/metrics/summary`
- **Output fields**: Total feedback counts, average rating, helpful/not helpful tallies, and fallback status.

## What Is Not Logged
- Raw CV files, upload binary data, and profile contents.
- Prompt injection inputs (which are redirected/redacted).
- System-level secrets and third-party API credentials.

## Limitations
This system implements lightweight file/console structured logging for local process observability. It does not integrate external agents (e.g. Sentry or Prometheus) to maintain zero external network dependencies.
