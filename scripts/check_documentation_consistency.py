#!/usr/bin/env python
"""Documentation consistency checker for CareerVerse Agent Capstone."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_README_SECTIONS = [
    "CareerVerse Agent",
    "Track",
    "Problem",
    "Solution",
    "Why Agents?",
    "Key Course Concepts Demonstrated",
    "Architecture",
    "Features",
    "Tech Stack",
    "Project Structure",
    "Setup",
    "Run the API",
    "API Usage",
    "Example Request",
    "Example Response",
    "Local Evaluation",
    "Testing",
    "Security and Responsible AI",
    "Dataset",
    "Agent Skills",
    "MCP-Style Tool Server",
    "Limitations",
    "Future Work",
    "Kaggle Submission Notes",
    "License"
]

FORBIDDEN_PATTERNS = [
    (r"production database is implemented", "Claims production database is implemented"),
    (r"Neo4j is implemented", "Claims Neo4j is implemented"),
    (r"pgvector is implemented", "Claims pgvector is implemented"),
    (r"real Gemini integration is implemented", "Claims real Gemini is implemented"),
    (r"CV parser is implemented", "Claims CV parser is implemented"),
    (r"voice inference is implemented", "Claims voice inference is implemented"),
    (r"market crawler is implemented", "Claims market crawler is implemented"),
    (r"payment is implemented", "Claims payment is implemented"),
    (r"authentication is implemented", "Claims authentication is implemented"),
    (r"live deployment is implemented", "Claims live deployment is implemented"),
    (r"cloud deployment is live", "Claims cloud deployment is live"),
]

def check_file_exists(path: Path) -> bool:
    if not path.exists():
        print(f"FAIL: File does not exist: {path.relative_to(ROOT)}")
        return False
    return True

def count_words(text: str) -> int:
    # Strip markdown formatting for basic word count
    clean_text = re.sub(r'[#\-\*\`\[\]\(\)\>\!\:\d\.]', ' ', text)
    words = clean_text.split()
    return len(words)

def main() -> int:
    failures = 0

    print("=== STARTING DOCUMENTATION CONSISTENCY AUDIT ===")

    # 1. Check files exist
    readme_path = ROOT / "README.md"
    arch_path = ROOT / "docs" / "architecture.md"
    demo_script_path = ROOT / "docs" / "demo_script.md"
    writeup_path = ROOT / "docs" / "writeup.md"
    checklist_path = ROOT / "docs" / "submission_checklist.md"
    runtime_path = ROOT / "docs" / "runtime.md"

    files_to_check = [
        readme_path,
        arch_path,
        demo_script_path,
        writeup_path,
        checklist_path,
        runtime_path
    ]
    for f in files_to_check:
        if not check_file_exists(f):
            failures += 1

    if failures > 0:
        print("FAIL: Core documentation files are missing.")
        return 1

    # Read contents
    readme_content = readme_path.read_text(encoding="utf-8")
    arch_content = arch_path.read_text(encoding="utf-8")
    writeup_content = writeup_path.read_text(encoding="utf-8")
    runtime_content = runtime_path.read_text(encoding="utf-8")
    
    # 2. Check README headings
    print("\nChecking README.md headings:")
    for section in REQUIRED_README_SECTIONS:
        # Check if the section name appears as a heading or substring
        # We search case-insensitively or as regular markdown headings
        pattern = re.compile(rf"#.*\b{re.escape(section)}\b", re.IGNORECASE)
        # Fallback to simple substring search if regex is too strict
        if not pattern.search(readme_content) and section.lower() not in readme_content.lower():
            print(f"FAIL: Missing required README section/content matching '{section}'")
            failures += 1
        else:
            print(f"  PASS: Section '{section}' found")

    # 3. Check Writeup word count
    print("\nChecking docs/writeup.md word count:")
    word_cnt = count_words(writeup_content)
    print(f"  Word count: {word_cnt} words")
    if word_cnt > 2500:
        print(
            f"FAIL: docs/writeup.md has {word_cnt} words, "
            f"which exceeds the 2500 word limit."
        )
        failures += 1
    else:
        print("  PASS: Word count within limits")

    # 4. Check for forbidden claims of unimplemented features in README & Writeup
    print("\nChecking for forbidden feature claims:")
    all_docs_content = readme_content + "\n" + arch_content + "\n" + writeup_content
    for pattern, message in FORBIDDEN_PATTERNS:
        match = re.search(pattern, all_docs_content, re.IGNORECASE)
        if match:
            print(f"FAIL: Forbidden claim detected: '{match.group(0)}' ({message})")
            failures += 1
        else:
            print(f"  PASS: No claim matching '{pattern}'")

    # 5. Check README for specific details: safety notice, evaluation command, setup command
    print("\nChecking required README content elements:")
    
    # Safety notice checking
    safety_notice_str = (
        "This system provides educational career guidance only. It does not "
        "guarantee employment outcomes or replace professional counseling."
    )
    if safety_notice_str.lower() not in readme_content.lower():
        print("FAIL: Safety notice is missing or incorrect in README.")
        failures += 1
    else:
        print("  PASS: Safety notice found")

    # Setup command checking
    if "pip install -r requirements.txt" not in readme_content:
        print("FAIL: Setup instructions ('pip install -r requirements.txt') not found in README.")
        failures += 1
    else:
        print("  PASS: Setup command found")

    # Evaluation command checking
    if "python -m app.evals.evaluate_agent" not in readme_content:
        print(
            "FAIL: Local evaluation command "
            "('python -m app.evals.evaluate_agent') not found in README."
        )
        failures += 1
    else:
        print("  PASS: Evaluation command found")

    # Docker Runtime check in README
    if "Docker Runtime".lower() not in readme_content.lower():
        print("FAIL: 'Docker Runtime' section not found in README.")
        failures += 1
    if "docker build" not in readme_content:
        print("FAIL: 'docker build' command not found in README.")
        failures += 1
    if "docker compose up --build" not in readme_content:
        print("FAIL: 'docker compose up --build' command not found in README.")
        failures += 1
    if "python scripts/docker_smoke_check.py" not in readme_content:
        print("FAIL: 'python scripts/docker_smoke_check.py' command not found in README.")
        failures += 1

    # runtime.md verification checks
    print("\nChecking docs/runtime.md content elements:")
    required_runtime_elements = [
        ("Docker Runtime", "Docker Runtime section missing in runtime.md"),
        ("Environment Variables", "Environment Variables section missing in runtime.md"),
        ("Health Checks", "Health Checks section missing in runtime.md"),
        ("Do not commit .env", "Do not commit .env safety advice missing in runtime.md"),
    ]
    for element, error_msg in required_runtime_elements:
        if element.lower() not in runtime_content.lower():
            print(f"FAIL: {error_msg}")
            failures += 1
        else:
            print(f"  PASS: runtime.md contains '{element}'")

    # 6. Check if docs mention "implemented vs future work"
    if "future work" not in readme_content.lower() or "future work" not in writeup_content.lower():
        print("FAIL: 'Future Work' section missing or not clearly documented.")
        failures += 1
    else:
        print("  PASS: Future work clearly demarcated")

    # 7. Check for obvious credentials in docs
    print("\nChecking for obvious credentials in documentation:")
    cred_patterns = [
        r"api[-_]?key\s*=\s*['\"][a-zA-Z0-9]{20,}['\"]",
        r"pass" + r"word\s*=\s*['\"][a-zA-Z0-9_]{8,}['\"]",
        r"db_pass" + r"word",
    ]
    leak_detected = False
    for sp in cred_patterns:
        if re.search(sp, all_docs_content, re.IGNORECASE):
            leak_detected = True
            break
    if leak_detected:
        print("FAIL: Potential hardcoded credential found in docs.")
        failures += 1
    else:
        print("  PASS: No credentials found in docs")

    print("\n=== CONSISTENCY AUDIT SUMMARY ===")
    if failures > 0:
        print(f"RESULT: FAIL ({failures} issues found)")
        return 1
    else:
        print("RESULT: PASS")
        return 0

if __name__ == "__main__":
    sys.exit(main())
