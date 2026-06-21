# API Versioning Guide

## Overview
This document describes the API versioning strategy, directory layout, endpoint mapping, error response contract, and safety behaviors introduced in the CareerVerse Agent system. It ensures the API is professional, extensible, and clean while maintaining 100% backward compatibility with legacy clients.

---

## Why Versioned APIs?
As the CareerVerse Agent platform evolves, API contracts may change. Versioning under `/api/v1` helps:
- Prevent breaking existing frontend clients and automated integrations.
- Support parallel evolution of experimental (legacy) and stabilized (versioned) features.
- Cleanly separate newer structured error contracts from FastAPI's default handlers.

---

## Current Version
The current active API version is **v1** (located under [app/api/v1/](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1)). All stabilization changes are targeting `/api/v1/...`.

---

## Legacy Endpoint Compatibility
Legacy endpoints (e.g., `/recommend`, `/metadata`, `/tools`, and `/mcp/*`) remain active and fully functional. They route directly to underlying business logic helpers without code duplication, ensuring zero business logic regression.

---

## Versioned Endpoint Map

| HTTP Method | Legacy Endpoint | Versioned Equivalent | Description | Tags |
|---|---|---|---|---|
| `GET` | `/` | `/api/v1/health` | Service status health check | `Health` |
| `GET` | `/metadata` | `/api/v1/metadata` | System version and capstone metadata | `Health` |
| `POST` | `/profiles/validate` | `/api/v1/profiles/validate` | Validation and normalization check | `Profiles` |
| `POST` | `/recommend` | `/api/v1/recommend` | Agent-orchestrated recommendation scoring | `Recommendations` |
| `GET` | `/tools` | `/api/v1/tools` | Enumeration of registered MCP tools | `MCP Tools` |
| `GET` | `/mcp/careers` | `/api/v1/mcp/careers` | List careers with paging limits | `MCP Tools` |
| `GET` | `/mcp/careers/{id}` | `/api/v1/mcp/careers/{id}` | Retrieve individual career information | `MCP Tools` |
| `GET` | `/mcp/careers/{id}/skills` | `/api/v1/mcp/careers/{id}/skills` | Retrieve skills required for a career | `MCP Tools` |
| `GET` | `/mcp/careers/{id}/roadmap` | `/api/v1/mcp/careers/{id}/roadmap` | Retrieve study roadmap for a career | `MCP Tools` |
| `GET` | `/mcp/skills` | `/api/v1/mcp/skills` | List skills with paging limits | `MCP Tools` |
| `GET` | `/mcp/skills/{name}` | `/api/v1/mcp/skills/{name}` | Retrieve individual skill details | `MCP Tools` |
| `GET` | `/mcp/search/careers` | `/api/v1/mcp/search/careers` | Search career titles matching query `q` | `MCP Tools` |
| `GET` | `/mcp/search/skills` | `/api/v1/mcp/search/skills` | Search skill names matching query `q` | `MCP Tools` |
| `POST` | N/A | `/api/v1/safety/validate-profile` | Safety and redaction validation endpoint | `Safety` |

---

## Error Response Contract
For versioned `v1` routes, all validation or application errors are structured under a standard `ErrorResponse` schema (defined in [error_schema.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/schemas/error_schema.py)).

### ErrorResponse Schema
```json
{
  "error": "ErrorTypeString",
  "message": "Human readable summary of the error",
  "status_code": 400,
  "details": null
}
```

- **Validation Errors (422)**: Standard FastAPI schema validation errors are intercepted and rewritten into this unified format to prevent exposing raw framework internals.
- **Resource Not Found (404)**: Triggers when querying careers or skills that do not exist (mapped from `ResourceNotFoundError`).
- **Unsafe Profile Block (400)**: Triggers when prompt injection attempts are detected in profile inputs (mapped from `UnsafeProfileError`).

---

## Safety Behavior
The safety layer acts defensively at the boundary of versioned routes:
1. **Denylist Interception**: If raw input contains forbidden keywords (like *"ignore previous instructions"*), an `UnsafeProfileError` is thrown.
2. **No Input Echoing**: The response payload does not repeat or reflect the malicious input, preventing echo-based exploits.
3. **Graceful Redaction**: Sensitives like authorization headers or API keys are scrubbed and replaced with placeholders (e.g., `[REDACTED]`).

---

## Migration Notes
- All new API consumers (such as frontend dashboards or LLM runtime layers) MUST query `/api/v1/...` routes.
- Legacy endpoints are maintained for backward compatibility. Note that legacy endpoints may still throw default FastAPI 422 errors, while versioned endpoints return the standardized `ErrorResponse` contract.

---

## Testing Commands
Validate the API and versioning behavior via the following test runners:
```bash
# Run versioning and error contract pytest suites
pytest tests/test_api_versioning.py tests/test_error_contract.py

# Run offline endpoint smoke test script
python scripts/smoke_test_api.py
```
