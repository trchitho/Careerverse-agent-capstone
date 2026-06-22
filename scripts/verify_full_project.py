#!/usr/bin/env python
"""Unified Quality Gate execution runner for the CareerVerse Agent Capstone."""

from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IS_WINDOWS = platform.system() == "Windows"


def run_command(cmd: list[str], cwd: Path = ROOT) -> bool:
    """Execute a system command and return True on success, False on failure."""
    use_shell = IS_WINDOWS
    cmd_str = " ".join(cmd)
    print(f"Running quality gate: {cmd_str}...")
    
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
        print(f"  -> ERROR: Execution failed: {exc}\n")
        return False


def main() -> int:
    print("=== EXECUTING FULL PROJECT QUALITY GATES ===\n")
    failures = 0

    # Command checklist
    commands = [
        [sys.executable, "scripts/validate_domain_dataset.py"],
        [sys.executable, "scripts/audit_prompt_0_to_7.py"],
        [sys.executable, "scripts/smoke_test_api.py"],
        [sys.executable, "-m", "app.evals.evaluate_agent"],
        [sys.executable, "-m", "app.evals.fr_nfr.run_fr_nfr_verification"],
        [sys.executable, "scripts/check_documentation_consistency.py"],
        [sys.executable, "scripts/pre_deploy_check.py"],
        [sys.executable, "-m", "compileall", "app"],
        ["ruff", "check", "."],
        ["pytest"],
    ]

    for cmd in commands:
        if not run_command(cmd):
            failures += 1

    # Web compilation check
    web_dir = ROOT / "web"
    if (web_dir / "package.json").is_file():
        if not run_command(["npm", "run", "build"], cwd=web_dir):
            failures += 1

    print("=== QUALITY GATE VERIFICATION SUMMARY ===")
    if failures > 0:
        print(f"RESULT: FAIL ({failures} checks failed)")
        return 1
    else:
        print("RESULT: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())
