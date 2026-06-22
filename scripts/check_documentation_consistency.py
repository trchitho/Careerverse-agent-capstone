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
    (r"legacy endpoints? (have been )?removed", "Claims legacy endpoints removed"),
    (r"full production auth", "Claims full production auth"),
    (r"PostgreSQL is implemented", "Claims PostgreSQL is implemented"),
    (r"full auth is implemented", "Claims full auth is implemented"),
    (r"sensitive personal data is stored", "Claims sensitive personal data is stored"),
    (r"sensitive user data is stored", "Claims sensitive user data is stored"),
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
    api_versioning_path = ROOT / "docs" / "api_versioning.md"
    api_examples_path = ROOT / "docs" / "api_examples.md"
    persistence_plan_path = ROOT / "docs" / "persistence_plan.md"
    explanation_service_path = ROOT / "docs" / "explanation_service.md"
    session_storage_path = ROOT / "docs" / "session_storage.md"
    frontend_path = ROOT / "docs" / "frontend.md"
    observability_path = ROOT / "docs" / "observability.md"
    feedback_analytics_path = ROOT / "docs" / "feedback_analytics.md"

    files_to_check = [
        readme_path,
        arch_path,
        demo_script_path,
        writeup_path,
        checklist_path,
        runtime_path,
        api_versioning_path,
        api_examples_path,
        persistence_plan_path,
        explanation_service_path,
        session_storage_path,
        frontend_path,
        observability_path,
        feedback_analytics_path,
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
    api_versioning_content = api_versioning_path.read_text(encoding="utf-8")
    api_examples_content = api_examples_path.read_text(encoding="utf-8")
    persistence_plan_content = persistence_plan_path.read_text(encoding="utf-8")
    explanation_service_content = explanation_service_path.read_text(encoding="utf-8")
    session_storage_content = session_storage_path.read_text(encoding="utf-8")
    frontend_content = frontend_path.read_text(encoding="utf-8")
    observability_content = observability_path.read_text(encoding="utf-8")
    feedback_analytics_content = feedback_analytics_path.read_text(encoding="utf-8")
    
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
    all_docs_content = (
        readme_content + "\n" +
        arch_content + "\n" +
        writeup_content + "\n" +
        api_versioning_content + "\n" +
        api_examples_content + "\n" +
        persistence_plan_content + "\n" +
        explanation_service_content + "\n" +
        session_storage_content + "\n" +
        frontend_content + "\n" +
        observability_content + "\n" +
        feedback_analytics_content
    )
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

    # API Versioning checks
    print("\nChecking API versioning content elements:")
    if "API Versioning".lower() not in readme_content.lower():
        print("FAIL: 'API Versioning' section not found in README.")
        failures += 1
    else:
        print("  PASS: README contains 'API Versioning'")

    if "/api/v1/recommend" not in readme_content:
        print("FAIL: '/api/v1/recommend' not found in README.")
        failures += 1
    else:
        print("  PASS: README contains '/api/v1/recommend'")

    if "/api/v1" not in api_examples_content:
        print("FAIL: '/api/v1' examples not found in docs/api_examples.md.")
        failures += 1
    else:
        print("  PASS: docs/api_examples.md contains '/api/v1'")

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

    # 6b. Repository and Persistence consistency checks
    print("\nChecking persistence, explanation, and saved recommendations assertions:")
    if "data access and persistence readiness" not in readme_content.lower():
        print("FAIL: README does not mention repository layer / persistence readiness.")
        failures += 1
    if "optional explanation service" not in readme_content.lower():
        print("FAIL: README does not mention optional explanation service.")
        failures += 1
    if (
        "llm-based explanations are optional and disabled" not in readme_content.lower()
        and "disabled by default" not in readme_content.lower()
    ):
        print("FAIL: README does not state external LLM is disabled by default.")
        failures += 1
    if "does not implement full authentication" not in readme_content.lower():
        print("FAIL: README does not state no production authentication.")
        failures += 1

    # 6c. Web UI, Observability, and Feedback assertions
    print("\nChecking Web UI, Observability, and Feedback assertions:")
    if "web ui" not in readme_content.lower():
        print("FAIL: README does not mention Web UI.")
        failures += 1
    if "vite_api_base_url" not in readme_content.lower():
        print("FAIL: README does not mention VITE_API_BASE_URL.")
        failures += 1
    if "observability" not in readme_content.lower():
        print("FAIL: README does not mention Observability.")
        failures += 1
    if "feedback analytics" not in readme_content.lower():
        print("FAIL: README does not mention Feedback Analytics.")
        failures += 1
    if (
        "request bodies" not in all_docs_content.lower()
        or "not logged" not in all_docs_content.lower()
    ):
        print("FAIL: Documentation does not assert that request bodies are not logged.")
        failures += 1
    if (
        "inmemoryfeedbackrepository" not in all_docs_content.lower()
        and "in-memory" not in all_docs_content.lower()
    ):
        print("FAIL: Documentation does not state feedback storage is local/demo/in-memory.")
        failures += 1

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
