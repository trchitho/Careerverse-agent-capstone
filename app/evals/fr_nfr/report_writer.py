"""Report writer for requirements verification summary reports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json_report(summary: dict[str, Any], path: Path) -> None:
    """Write the verification summary as a JSON file."""
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def write_markdown_report(summary: dict[str, Any], path: Path) -> None:
    """Write the verification summary as a Markdown file."""
    title = "# FR/NFR Requirements Verification Summary Report\n\n"
    
    # 1. Summary details
    md_content = [
        title,
        "## Overall Verdict",
        f"**Verdict**: {summary.get('final_verdict', 'FAIL')}\n",
        "## Summary Metrics",
        f"- **Total FR Requirements**: {summary.get('total_fr_requirements', 0)}",
        f"- **Total NFR Requirements**: {summary.get('total_nfr_requirements', 0)}",
        f"- **Total FR Test Cases**: {summary.get('total_fr_cases', 0)}",
        f"- **Total NFR Test Cases**: {summary.get('total_nfr_cases', 0)}",
        f"- **Passed Cases**: {summary.get('passed_cases', 0)}",
        f"- **Failed Cases**: {summary.get('failed_cases', 0)}",
        f"- **Pass Rate**: {summary.get('pass_rate', 0.0):.2f}%\n",
    ]
    
    # 2. Checklist requirement issues
    under_limit = summary.get("requirements_with_less_than_50_cases", [])
    if under_limit:
        md_content.append("## Requirements with Less Than 50 Cases")
        for req in under_limit:
            md_content.append(f"- {req}")
        md_content.append("")
        
    failed_reqs = summary.get("failed_requirements", [])
    if failed_reqs:
        md_content.append("## Failed Requirements")
        for req in failed_reqs:
            md_content.append(f"- {req}")
        md_content.append("")
        
    # 3. Findings
    sec_findings = summary.get("security_findings", [])
    if sec_findings:
        md_content.append("## Security Findings")
        for finding in sec_findings:
            md_content.append(f"- {finding}")
        md_content.append("")
        
    doc_findings = summary.get("documentation_findings", [])
    if doc_findings:
        md_content.append("## Documentation Findings")
        for finding in doc_findings:
            md_content.append(f"- {finding}")
        md_content.append("")
        
    path.write_text("\n".join(md_content), encoding="utf-8")


def format_requirement_summary(req_id: str, passed: int, total: int) -> str:
    """Format requirement statistics as a string."""
    return f"Requirement {req_id}: {passed}/{total} passed"


def format_failed_cases(failed_cases: list[dict[str, Any]]) -> str:
    """Format the list of failed cases into a readable log string."""
    lines = []
    for c in failed_cases:
        case_id = c.get("case_id")
        req_id = c.get("requirement_id")
        msg = c.get("message")
        lines.append(f"FAIL: Case ID {case_id} ({req_id}) - {msg}")
    return "\n".join(lines)
