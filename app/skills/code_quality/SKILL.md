---
name: code-quality
description: Review and improve CareerVerse Agent code quality. Use before finalizing changes to FastAPI endpoints, Pydantic schemas, agent orchestration, tools, evaluation scripts, tests, or documentation examples.
---

# Code Quality Skill

## Purpose

Review and improve code quality for the CareerVerse Agent project.

## When to Use

Use this skill before finalizing any implementation task, especially when modifying:

- FastAPI endpoints
- Pydantic schemas
- Agent orchestration
- Tools
- Evaluation scripts
- Documentation examples

## Checklist

Check:

- Code is readable.
- Functions are small.
- Type hints are used.
- Imports are clean.
- No dead code exists.
- No duplicated logic exists.
- Error handling is safe.
- Public behavior is documented.
- Tests are added or updated when relevant.
- README is updated when behavior changes.

## Commands

Run when possible:

```bash
python -m compileall app
ruff check .
pytest
```

## Output

Report:

* Files reviewed
* Issues fixed
* Commands run
* Remaining known issues
