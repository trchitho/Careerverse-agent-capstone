# Git Workflow Rules

## Mandatory Commit Frequency

After every 10–30 lines of real code changes:

```bash
git add .
git commit -m "<appropriate message>"
```

This is mandatory.

Do not reinterpret it as “commit after a meaningful small change.”

## Commit Style

Use short, clear messages.

Examples:

```text
chore: add project rules
docs: add security rules
chore: add agent skill docs
test: add health endpoint test
fix: clean ruff issues
```

The coding agent chooses the message without asking the user.

## Push Rule

Push only once at the end:

```bash
git push origin main
```

If remote `origin` is missing, report it honestly.

## Before Final Response

Run:

```bash
git status
```

If changes remain:

```bash
git add .
git commit -m "<appropriate message>"
```

Then push once if remote exists.
