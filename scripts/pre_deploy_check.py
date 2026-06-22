#!/usr/bin/env python
"""Pre-deployment verification runner for CareerVerse Agent Capstone."""

from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IS_WINDOWS = platform.system() == "Windows"


def run_command(cmd: list[str] | str, cwd: Path = ROOT) -> bool:
    """Run a system command and return True if exit code is 0."""
    # On Windows, command scripts (ruff, pytest, npm) require shell=True
    use_shell = IS_WINDOWS if isinstance(cmd, list) else True
    
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
    print(f"Running: {cmd_str} (in {cwd.relative_to(ROOT) or '.'})...")
    
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd),
            shell=use_shell,
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            print("  -> PASS")
            return True
        else:
            print(f"  -> FAIL (Exit Code: {res.returncode})")
            print(f"--- STDOUT ---\n{res.stdout}")
            print(f"--- STDERR ---\n{res.stderr}\n")
            return False
    except Exception as exc:
        print(f"  -> ERROR: Failed to execute: {exc}\n")
        return False


def main() -> int:
    """Run all quality gates and exit with 0 if all pass, or 1 if any fail."""
    print("=== STARTING PRE-DEPLOYMENT VERIFICATION GATE ===\n")
    failures = 0

    # 1. Dataset Verification
    if not run_command([sys.executable, "scripts/validate_domain_dataset.py"]):
        failures += 1

    # 2. Compileall app
    if not run_command([sys.executable, "-m", "compileall", "app"]):
        failures += 1

    # 3. Ruff linter
    if not run_command(["ruff", "check", "."]):
        failures += 1

    # 4. Pytest suite
    if not run_command(["pytest"]):
        failures += 1

    # 5. Model offline evaluations
    if not run_command([sys.executable, "-m", "app.evals.evaluate_agent"]):
        failures += 1

    # 6. API smoke tests
    if not run_command([sys.executable, "scripts/smoke_test_api.py"]):
        failures += 1

    # 7. Documentation consistency
    if not run_command([sys.executable, "scripts/check_documentation_consistency.py"]):
        failures += 1

    # 8. Web frontend compilation check
    web_dir = ROOT / "web"
    if (web_dir / "package.json").is_file():
        # First check if build outputs exist but are ignored
        dist_dir = web_dir / "dist"
        if dist_dir.exists():
            print("WARNING: Frontend build folder 'web/dist' already exists locally.")
            print("Ensure it is ignored by git and not tracked.")
            
        if not run_command(["npm", "run", "build"], cwd=web_dir):
            failures += 1

    print("=== PRE-DEPLOYMENT VERIFICATION SUMMARY ===")
    if failures > 0:
        print(f"RESULT: FAIL ({failures} gates failed)")
        return 1
    else:
        print("RESULT: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())
