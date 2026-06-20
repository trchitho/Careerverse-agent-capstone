# Code Quality Rules

## Python

Use Python 3.11+.

Rules:

- Use type hints for public functions.
- Use Pydantic models for API schemas.
- Use Pydantic Settings for configuration.
- Keep functions small and focused.
- Avoid global mutable state unless justified.
- Avoid duplicated logic.
- Avoid unused imports.
- Avoid dead code.
- Prefer deterministic behavior for recommendation logic.
- Keep comments useful, not noisy.

## FastAPI

Rules:

- Keep app entrypoint in `app/main.py`.
- Keep config in `app/core/config.py`.
- Keep constants in `app/core/constants.py`.
- Keep schemas in `app/schemas/`.
- Keep orchestration in `app/agents/`.
- Keep deterministic helper logic in `app/tools/`.
- Keep local MCP-style resources in `app/mcp_server/`.

## Error Handling

- Return safe error messages.
- Do not expose secrets.
- Do not expose internal stack traces in API responses.
- Avoid swallowing errors silently.

## Validation Commands

Run when possible:

```bash
python -m compileall app
ruff check .
pytest
```
