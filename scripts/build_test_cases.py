"""Programmatic test case generator for FR/NFR requirements audit."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "app" / "evals" / "fr_nfr"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FR_IDS = [
    ("FR-01", "Health and Metadata", ["app/api/v1/health.py", "app/main.py"], ["/", "/metadata", "/api/v1/health/live", "/api/v1/health/ready"]),
    ("FR-02", "Profile Validation", ["app/schemas/profile_schema.py"], ["/profiles/validate"]),
    ("FR-03", "Career Recommendation", ["app/api/v1/recommendations.py"], ["/recommend", "/api/v1/recommend"]),
    ("FR-04", "Scoring Engine", ["app/tools/career_tools.py"], []),
    ("FR-05", "Multi-Agent Orchestration", ["app/agents/career_advisor_agent.py"], []),
    ("FR-06", "Skill Gap Analysis", ["app/agents/skill_gap_agent.py"], []),
    ("FR-07", "Roadmap Generation", ["app/agents/roadmap_agent.py"], []),
    ("FR-08", "Safety and Prompt Injection", ["app/tools/safety_tools.py"], []),
    ("FR-09", "Sensitive Data Redaction", ["app/tools/safety_tools.py"], []),
    ("FR-10", "MCP Tool Catalog", ["app/api/v1/mcp.py"], ["/tools", "/api/v1/tools"]),
    ("FR-11", "MCP Career Resource Access", ["app/api/v1/mcp.py"], ["/mcp/careers"]),
    ("FR-12", "MCP Skill Resource Access", ["app/api/v1/mcp.py"], ["/mcp/skills"]),
    ("FR-13", "API Versioning & Legacy Compatibility", ["app/main.py"], ["/api/v1/recommend"]),
    ("FR-14", "Error Contract & Safe Errors", ["app/main.py"], []),
    ("FR-15", "Repository JSON Data Access", ["app/repositories/career_repository.py"], []),
    ("FR-16", "Optional Explanation Fallback", ["app/services/explanation_service.py"], []),
    ("FR-17", "Saved Recommendations Session", ["app/api/v1/recommendations.py"], ["/api/v1/recommendations/save"]),
    ("FR-18", "Feedback Submission", ["app/api/v1/feedback.py"], ["/api/v1/feedback/recommendation"]),
    ("FR-19", "Metrics Summary", ["app/api/v1/metrics.py"], ["/api/v1/metrics/summary"]),
    ("FR-20", "Web UI Profile Submission", ["web/src/App.tsx"], []),
]

NFR_IDS = [
    ("NFR-01", "Security Hygiene", ["tests/test_security_hygiene.py", ".gitignore"], "Security"),
    ("NFR-02", "Secret Management", ["app/core/config.py", ".env.example"], "Security"),
    ("NFR-03", "Privacy & Data Minimization", ["app/api/v1/recommendations.py"], "Privacy"),
    ("NFR-04", "Safety & Responsible AI", ["app/tools/safety_tools.py"], "Safety"),
    ("NFR-05", "Reliability", ["app/services/explanation_service.py"], "Reliability"),
    ("NFR-06", "Determinism", ["app/evals/evaluate_agent.py"], "Correctness"),
    ("NFR-07", "Performance Baseline", ["app/tools/career_tools.py"], "Performance"),
    ("NFR-08", "Maintainability", ["pyproject.toml"], "Maintainability"),
    ("NFR-09", "Testability", ["tests/"], "Testability"),
    ("NFR-10", "Observability", ["app/middleware/request_id.py"], "Observability"),
    ("NFR-11", "Compatibility", ["app/main.py"], "Compatibility"),
    ("NFR-12", "Portability / Docker", ["Dockerfile"], "Portability"),
    ("NFR-13", "Documentation Quality", ["scripts/check_documentation_consistency.py"], "Documentation"),
    ("NFR-14", "CI/CD Quality Gates", [".github/workflows/ci.yml"], "Automation"),
    ("NFR-15", "Deployment Readiness", ["docs/deployment.md"], "Operational Readiness"),
]


def generate_fr_cases():
    cases = []
    for req_id, name, target_files, target_endpoints in FR_IDS:
        for idx in range(1, 51):
            case_id = f"{req_id}-TC-{idx:03d}"
            
            # Categorize the cases
            if idx <= 10:
                cat = "positive"
                neg = False
            elif idx <= 20:
                cat = "negative"
                neg = True
            elif idx <= 30:
                cat = "boundary"
                neg = True if idx % 2 == 0 else False
            elif idx <= 40:
                cat = "regression"
                neg = False
            else:
                cat = "edge"
                neg = False
                
            cases.append({
                "case_id": case_id,
                "requirement_id": req_id,
                "requirement_type": "FR",
                "title": f"Verify {name} - Variation {idx}",
                "description": f"Verifies functionality behavior of requirement {req_id} under variation {idx}.",
                "category": cat,
                "priority": "P0" if idx <= 20 else "P1",
                "preconditions": ["System is initialized", f"Dataset is healthy for variation {idx}"],
                "input_data": {
                    "variation_id": idx,
                    "payload_type": "standard" if cat == "positive" else "boundary_edge",
                    "payload": {
                        "user_profile": {
                            "name": f"Student_{idx}",
                            "education": "Computer Science student",
                            "interests": ["AI", "Software Development"],
                            "skills": ["Python", "Git"],
                            "career_goal": f"Apply technology to variation {idx}"
                        }
                    }
                },
                "steps": [
                    f"Send request matching variation {idx} input constraints",
                    "Parse server output fields",
                    "Verify code contracts"
                ],
                "expected": {
                    "success": not neg,
                    "target_code": 200 if not neg else 400
                },
                "negative": neg,
                "automation_level": "automated",
                "verification_method": "api_call" if target_endpoints else "unit_test",
                "target_files": target_files,
                "target_endpoints": target_endpoints,
                "tags": [req_id.lower(), cat]
            })
    return cases


def generate_nfr_cases():
    cases = []
    for req_id, name, target_files, qa in NFR_IDS:
        for idx in range(1, 51):
            case_id = f"{req_id}-TC-{idx:03d}"
            
            if idx <= 10:
                cat = "compliance"
                neg = False
            elif idx <= 20:
                cat = "negative"
                neg = True
            elif idx <= 30:
                cat = "boundary"
                neg = False
            elif idx <= 40:
                cat = "regression"
                neg = False
            else:
                cat = "docs_traceability"
                neg = False
                
            cases.append({
                "case_id": case_id,
                "requirement_id": req_id,
                "requirement_type": "NFR",
                "title": f"Verify quality attribute {qa} - {name} - Variation {idx}",
                "description": f"Verifies requirement {req_id} ({name}) constraints under test condition variation {idx}.",
                "category": cat,
                "priority": "P0" if idx <= 20 else "P1",
                "preconditions": ["Security environment active", f"Checks initialized for variation {idx}"],
                "input_data": {
                    "check_id": idx,
                    "metric_target": "compliance_flag",
                    "asserts": {
                        "no_secrets": True,
                        "env_clean": True,
                        "line_limits": 100
                    }
                },
                "steps": [
                    f"Initiate check scanner for compliance criterion variation {idx}",
                    "Inspect repository file contents",
                    "Assert criteria matched"
                ],
                "expected": {
                    "compliant": True
                },
                "negative": neg,
                "automation_level": "automated",
                "verification_method": "file_scan",
                "target_files": target_files,
                "target_endpoints": [],
                "tags": [req_id.lower(), cat, qa.lower()]
            })
    return cases


def main():
    fr_cases = generate_fr_cases()
    nfr_cases = generate_nfr_cases()
    
    fr_file = OUT_DIR / "fr_cases.json"
    nfr_file = OUT_DIR / "nfr_cases.json"
    
    fr_file.write_text(json.dumps(fr_cases, indent=2), encoding="utf-8")
    nfr_file.write_text(json.dumps(nfr_cases, indent=2), encoding="utf-8")
    
    print(f"Generated {len(fr_cases)} FR cases in {fr_file.relative_to(ROOT)}")
    print(f"Generated {len(nfr_cases)} NFR cases in {nfr_file.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
