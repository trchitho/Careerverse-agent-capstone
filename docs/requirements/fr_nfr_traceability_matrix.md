# FR/NFR Traceability Matrix

This matrix maps Functional and Non-Functional Requirements to source code implementation, endpoints, and test cases.

| Req ID | Requirement Name | Source Files | API Endpoints | Test Case Range | Pytest Files | Status |
|---|---|---|---|---|---|---|
| **FR-01** | Health and Metadata | `app/api/v1/health.py`, `app/main.py` | `GET /`, `GET /metadata`, `GET /api/v1/health/live`, `GET /api/v1/health/ready` | `FR-01-TC-001` - `FR-01-TC-050` | `tests/test_health.py` | Implemented |
| **FR-02** | Profile Validation | `app/schemas/profile_schema.py`, `app/api/v1/recommend.py` | `POST /profiles/validate` | `FR-02-TC-001` - `FR-02-TC-050` | `tests/test_profile_validation_api.py` | Implemented |
| **FR-03** | Career Recommendation | `app/api/v1/recommend.py`, `app/main.py` | `POST /recommend`, `POST /api/v1/recommend` | `FR-03-TC-001` - `FR-03-TC-050` | `tests/test_recommend_api.py` | Implemented |
| **FR-04** | Scoring Engine | `app/core/career_scorer.py`, `app/tools/career_tools.py` | N/A (Internal) | `FR-04-TC-001` - `FR-04-TC-050` | `tests/test_career_tools.py` | Implemented |
| **FR-05** | Multi-Agent Orchestration | `app/agents/coordinator.py`, `app/agents/agent_workflow.py` | N/A (Internal) | `FR-05-TC-001` - `FR-05-TC-050` | `tests/test_agent_workflow.py` | Implemented |
| **FR-06** | Skill Gap Analysis | `app/agents/skill_gap_agent.py` | N/A (Internal) | `FR-06-TC-001` - `FR-06-TC-050` | `tests/test_skill_gap_agent.py` | Implemented |
| **FR-07** | Roadmap Generation | `app/agents/roadmap_agent.py` | N/A (Internal) | `FR-07-TC-001` - `FR-07-TC-050` | `tests/test_roadmap_agent.py` | Implemented |
| **FR-08** | Safety and Prompt Injection | `app/tools/safety_tools.py` | N/A (Internal) | `FR-08-TC-001` - `FR-08-TC-050` | `tests/test_safety_tools.py` | Implemented |
| **FR-09** | Sensitive Data Redaction | `app/tools/safety_tools.py`, `app/services/feedback_service.py` | N/A (Internal) | `FR-09-TC-001` - `FR-09-TC-050` | `tests/test_safety.py` | Implemented |
| **FR-10** | MCP Tool Catalog | `app/api/v1/mcp.py` | `GET /tools`, `GET /api/v1/tools` | `FR-10-TC-001` - `FR-10-TC-050` | `tests/test_mcp_api.py` | Implemented |
| **FR-11** | MCP Career Resource Access | `app/api/v1/mcp.py` | `GET /mcp/careers` | `FR-11-TC-001` - `FR-11-TC-050` | `tests/test_mcp_server.py` | Implemented |
| **FR-12** | MCP Skill Resource Access | `app/api/v1/mcp.py` | `GET /mcp/skills` | `FR-12-TC-001` - `FR-12-TC-050` | `tests/test_mcp_server.py` | Implemented |
| **FR-13** | API Versioning & Legacy | `app/main.py` | `/api/v1/*` | `FR-13-TC-001` - `FR-13-TC-050` | `tests/test_api_versioning.py` | Implemented |
| **FR-14** | Error Contract & Safe Errors | `app/main.py` | Global exception boundaries | `FR-14-TC-001` - `FR-14-TC-050` | `tests/test_error_contract.py` | Implemented |
| **FR-15** | Repository JSON Data Access | `app/repositories/career_repository.py` | N/A (Internal) | `FR-15-TC-001` - `FR-15-TC-050` | `tests/test_repositories.py` | Implemented |
| **FR-16** | Optional Explanation Fallback | `app/services/explanation_service.py` | N/A (Internal) | `FR-16-TC-001` - `FR-16-TC-050` | `tests/test_explanation_service.py` | Implemented |
| **FR-17** | Saved Recommendations Session | `app/api/v1/saved_recommendations.py` | `POST /api/v1/saved-recommendations`, `GET /api/v1/saved-recommendations` | `FR-17-TC-001` - `FR-17-TC-050` | `tests/test_saved_recommendations.py` | Implemented |
| **FR-18** | Feedback Submission | `app/api/v1/feedback.py`, `app/services/feedback_service.py` | `POST /api/v1/feedback/recommendation` | `FR-18-TC-001` - `FR-18-TC-050` | `tests/test_feedback_api.py` | Implemented |
| **FR-19** | Metrics Summary | `app/api/v1/metrics.py` | `GET /api/v1/metrics/summary` | `FR-19-TC-001` - `FR-19-TC-050` | `tests/test_feedback_api.py` | Implemented |
| **FR-20** | Web UI Profile Submission | `web/src/App.tsx`, `web/src/lib/apiClient.ts` | N/A (Frontend) | `FR-20-TC-001` - `FR-20-TC-050` | `tests/test_web_structure.py` | Implemented |
| **NFR-01** | Security Hygiene | `tests/test_security_hygiene.py`, `.gitignore`, `.dockerignore` | N/A | `NFR-01-TC-001` - `NFR-01-TC-050` | `tests/test_security_hygiene.py` | Implemented |
| **NFR-02** | Secret Management | `app/core/config.py`, `.env.example` | N/A | `NFR-02-TC-001` - `NFR-02-TC-050` | `tests/test_security_hygiene.py` | Implemented |
| **NFR-03** | Privacy & Data Minimization | `app/api/v1/saved_recommendations.py`, `app/schemas/feedback_schema.py` | N/A | `NFR-03-TC-001` - `NFR-03-TC-050` | `tests/test_saved_recommendations.py` | Implemented |
| **NFR-04** | Safety & Responsible AI | `app/tools/safety_tools.py`, `app/main.py` | N/A | `NFR-04-TC-001` - `NFR-04-TC-050` | `tests/test_safety.py` | Implemented |
| **NFR-05** | Reliability | `app/services/explanation_service.py` | N/A | `NFR-05-TC-001` - `NFR-05-TC-050` | `tests/test_explanation_service.py` | Implemented |
| **NFR-06** | Determinism | `app/evals/evaluate_agent.py` | N/A | `NFR-06-TC-001` - `NFR-06-TC-050` | `tests/test_evaluation_pipeline.py` | Implemented |
| **NFR-07** | Performance Baseline | `app/core/career_scorer.py` | N/A | `NFR-07-TC-001` - `NFR-07-TC-050` | `tests/test_recommend_api.py` | Implemented |
| **NFR-08** | Maintainability | `pyproject.toml`, `setup.cfg` | N/A | `NFR-08-TC-001` - `NFR-08-TC-050` | `tests/test_ci_workflows.py` | Implemented |
| **NFR-09** | Testability | `tests/`, `pytest.ini` | N/A | `NFR-09-TC-001` - `NFR-09-TC-050` | `tests/test_ci_workflows.py` | Implemented |
| **NFR-10** | Observability | `app/middleware/request_id.py`, `app/core/logging_config.py` | N/A | `NFR-10-TC-001` - `NFR-10-TC-050` | `tests/test_observability.py` | Implemented |
| **NFR-11** | Compatibility | `app/main.py` | `/api/v1/*` | `NFR-11-TC-001` - `NFR-11-TC-050` | `tests/test_api_versioning.py` | Implemented |
| **NFR-12** | Portability / Docker | `Dockerfile`, `docker-compose.yml`, `scripts/docker_smoke_check.py` | N/A | `NFR-12-TC-001` - `NFR-12-TC-050` | `tests/test_runtime_config.py` | Implemented |
| **NFR-13** | Documentation Quality | `scripts/check_documentation_consistency.py` | N/A | `NFR-13-TC-001` - `NFR-13-TC-050` | `tests/test_documentation.py` | Implemented |
| **NFR-14** | CI/CD Quality Gates | `.github/workflows/ci.yml`, `.github/workflows/security.yml` | N/A | `NFR-14-TC-001` - `NFR-14-TC-050` | `tests/test_ci_workflows.py` | Implemented |
| **NFR-15** | Deployment Readiness | `docs/deployment.md`, `docs/operations_runbook.md`, `scripts/pre_deploy_check.py` | N/A | `NFR-15-TC-001` - `NFR-15-TC-050` | `tests/test_deployment_docs.py` | Implemented |
