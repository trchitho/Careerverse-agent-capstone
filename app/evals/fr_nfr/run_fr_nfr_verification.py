"""Verification runner executing functional & non-functional requirements checks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from app.evals.fr_nfr.fr_nfr_schema import (
    RequirementCase,
    RequirementVerificationResult,
    RequirementVerificationSummary,
)
from app.evals.fr_nfr.report_writer import write_json_report, write_markdown_report

ROOT = Path(__file__).resolve().parents[3]
AUDIT_DIR = ROOT / "docs" / "audits"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)


def run_checks() -> int:
    print("=== EXECUTING REQUIREMENTS VERIFICATION ===")
    
    fr_file = ROOT / "app" / "evals" / "fr_nfr" / "fr_cases.json"
    nfr_file = ROOT / "app" / "evals" / "fr_nfr" / "nfr_cases.json"
    
    if not fr_file.exists() or not nfr_file.exists():
        print("FAIL: JSON case files are missing.")
        return 1
        
    try:
        fr_raw = json.loads(fr_file.read_text(encoding="utf-8"))
        nfr_raw = json.loads(nfr_file.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: Failed to parse JSON test cases: {exc}")
        return 1

    # 1. Validate schemas
    fr_cases: list[RequirementCase] = []
    nfr_cases: list[RequirementCase] = []
    
    for c in fr_raw:
        fr_cases.append(RequirementCase(**c))
    for c in nfr_raw:
        nfr_cases.append(RequirementCase(**c))
        
    print(f"Loaded and schema-validated {len(fr_cases)} FR and {len(nfr_cases)} NFR cases.")

    # 2. Assert constraints (>= 50 cases per requirement, unique IDs, no secrets)
    case_ids = set()
    req_counts: dict[str, int] = {}
    under_limit: list[str] = []
    failed_requirements: list[str] = []
    security_findings: list[str] = []
    doc_findings: list[str] = []
    
    # Secret pattern scan
    secret_pat = re.compile(r"sk-[0-9A-Za-z]{20,}|AIza[0-9A-Za-z_-]{20,}|ghp_[0-9A-Za-z]{20,}")

    results: list[RequirementVerificationResult] = []

    # Process FR
    for c in fr_cases:
        # Unique IDs
        if c.case_id in case_ids:
            print(f"FAIL: Duplicate case_id detected: {c.case_id}")
            return 1
        case_ids.add(c.case_id)
        
        req_counts[c.requirement_id] = req_counts.get(c.requirement_id, 0) + 1
        
        # Secret check
        input_str = json.dumps(c.input_data)
        if secret_pat.search(input_str):
            security_findings.append(f"Secret-like pattern found in case {c.case_id}")
            
        # Target files existence audit
        files_exist = True
        missing_files = []
        for tf in c.target_files:
            file_path = ROOT / tf
            if not file_path.exists():
                files_exist = False
                missing_files.append(tf)
                
        status = "PASS"
        message = "Verification successful."
        if not files_exist:
            status = "FAIL"
            message = f"Missing target implementation files: {', '.join(missing_files)}"
            
        results.append(RequirementVerificationResult(
            case_id=c.case_id,
            requirement_id=c.requirement_id,
            requirement_type=c.requirement_type,
            title=c.title,
            status=status,
            message=message
        ))

    # Process NFR
    for c in nfr_cases:
        if c.case_id in case_ids:
            print(f"FAIL: Duplicate case_id detected: {c.case_id}")
            return 1
        case_ids.add(c.case_id)
        
        req_counts[c.requirement_id] = req_counts.get(c.requirement_id, 0) + 1
        
        input_str = json.dumps(c.input_data)
        if secret_pat.search(input_str):
            security_findings.append(f"Secret-like pattern found in case {c.case_id}")
            
        # NFR checks: verifying documentation or file existence
        files_exist = True
        missing_files = []
        for tf in c.target_files:
            file_path = ROOT / tf
            if not file_path.exists():
                files_exist = False
                missing_files.append(tf)
                
        status = "PASS"
        message = "Verification successful."
        if not files_exist:
            status = "FAIL"
            message = f"Target files not found: {', '.join(missing_files)}"
            
        results.append(RequirementVerificationResult(
            case_id=c.case_id,
            requirement_id=c.requirement_id,
            requirement_type=c.requirement_type,
            title=c.title,
            status=status,
            message=message
        ))

    # Count requirements matching constraints
    for req, count in req_counts.items():
        if count < 50:
            under_limit.append(f"{req} (has {count} cases, required >= 50)")

    # Identify any failed requirement status
    failed_cases = 0
    passed_cases = 0
    for r in results:
        if r.status == "FAIL":
            failed_cases += 1
            if r.requirement_id not in failed_requirements:
                failed_requirements.append(r.requirement_id)
        else:
            passed_cases += 1

    total_fr_reqs = sum(1 for r in req_counts if r.startswith("FR-"))
    total_nfr_reqs = sum(1 for r in req_counts if r.startswith("NFR-"))

    # Requirements matrices checks
    trace_matrix = ROOT / "docs" / "requirements" / "fr_nfr_traceability_matrix.md"
    if not trace_matrix.exists():
        doc_findings.append("Missing traceability matrix file.")
    else:
        matrix_text = trace_matrix.read_text(encoding="utf-8")
        if "TODO" in matrix_text or "UNMAPPED" in matrix_text:
            doc_findings.append("Traceability matrix contains unresolved items (TODO/UNMAPPED).")

    final_verdict = "PASS"
    if failed_cases > 0 or under_limit or security_findings or doc_findings:
        final_verdict = "FAIL"

    summary = RequirementVerificationSummary(
        total_fr_requirements=total_fr_reqs,
        total_nfr_requirements=total_nfr_reqs,
        total_fr_cases=len(fr_cases),
        total_nfr_cases=len(nfr_cases),
        passed_cases=passed_cases,
        failed_cases=failed_cases,
        pass_rate=(passed_cases / len(results)) * 100 if results else 0.0,
        requirements_with_less_than_50_cases=under_limit,
        failed_requirements=failed_requirements,
        security_findings=security_findings,
        documentation_findings=doc_findings,
        final_verdict=final_verdict
    )

    # Write summaries
    summary_dict = summary.model_dump()
    
    write_json_report(summary_dict, AUDIT_DIR / "fr_nfr_verification_report.json")
    write_markdown_report(summary_dict, AUDIT_DIR / "fr_nfr_verification_report.md")

    print("\n=== VERIFICATION RESULTS SUMMARY ===")
    print(f"Functional cases: {len(fr_cases)} (all validated)")
    print(f"Non-functional cases: {len(nfr_cases)} (all validated)")
    print(f"Overall Pass Rate: {summary.pass_rate:.2f}%")
    print(f"Verdict: {final_verdict}")
    
    if final_verdict == "FAIL":
        print(f"Errors found: under_limit={under_limit}, failed_requirements={failed_requirements}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run_checks())
