# Non-Functional Requirements (NFR) Catalog

This catalog outlines the Non-Functional Requirements for the CareerVerse Agent system.

---

### NFR-01: Security Hygiene
- **Name**: Repository Secret Scan and Hygiene
- **Description**: Ensures that no static passwords, API tokens, or secrets reside in the source control repository.
- **Quality Attribute**: Security
- **Measurement Method**: Automated pre-commit scans and Git tracking reviews.
- **Acceptance Criteria**: Zero occurrences of private keys, GitHub PATs, Google Cloud API keys, or active credentials.
- **Negative Cases**: Commit triggers failure if `.env` files are accidentally indexed.
- **Related Tests**: `test_security_hygiene.py`
- **Status**: Implemented

---

### NFR-02: Secret Management
- **Name**: Decoupled Environment configuration
- **Description**: Configuration limits secrets from source control by parsing parameters via system environments.
- **Quality Attribute**: Security / Maintainability
- **Measurement Method**: File system tracking and .env.example audits.
- **Acceptance Criteria**: Excludes raw key values from all tracked codebases.
- **Negative Cases**: Fails execution if keys are hard-coded in configuration loaders.
- **Related Tests**: `test_security_hygiene.py`
- **Status**: Implemented

---

### NFR-03: Privacy and Data Minimization
- **Name**: Privacy Preservation Limits
- **Description**: Minimizes personal data exposure by omitting multi-user persistent credentials or authentication systems.
- **Quality Attribute**: Security / Privacy
- **Measurement Method**: Code inspections checking databases and user profiles.
- **Acceptance Criteria**: Replaces full signup records with client session identifiers.
- **Negative Cases**: Validates that no email, telephone, or home address fields are requested by the form.
- **Related Tests**: `test_full_project_security_regression.py`
- **Status**: Implemented

---

### NFR-04: Safety and Responsible AI
- **Name**: Guidance Disclaimers and Injection Interception
- **Description**: Provides standard educational advice disclaimers and flags instructions overrides.
- **Quality Attribute**: Safety
- **Measurement Method**: API response audits and input validation tests.
- **Acceptance Criteria**: Renders guidance notice in recommendations; blocks injection attempts with HTTP 400.
- **Negative Cases**: Returns HTTP 400 if career_goal or skills fields contain system override phrases.
- **Related Tests**: `test_safety.py`
- **Status**: Implemented

---

### NFR-05: Reliability
- **Name**: Graceful Fallback Mechanics
- **Description**: Resolves recommendation and explanation features even if external GenAI pipelines fail.
- **Quality Attribute**: Reliability
- **Measurement Method**: Error injection validation tests.
- **Acceptance Criteria**: Reverts back to local heuristic matches when API endpoints are unreachable.
- **Negative Cases**: Avoids throwing HTTP 500 errors if API connections are interrupted.
- **Related Tests**: `test_explanation_service.py`
- **Status**: Implemented

---

### NFR-06: Determinism
- **Name**: Calibrated Match Outputs
- **Description**: Ensures same profile inputs yield identical scoring matches without regression.
- **Quality Attribute**: Correctness / Quality
- **Measurement Method**: Offline evaluation pipelines.
- **Acceptance Criteria**: Achieving 100% calibration score in regression tests.
- **Negative Cases**: Evaluation triggers failures if match scores shift.
- **Related Tests**: `test_evaluation_pipeline.py`
- **Status**: Implemented

---

### NFR-07: Performance Baseline
- **Name**: Local Engine response Latencies
- **Description**: Response delays for local JSON matches remain low under single user scenarios.
- **Quality Attribute**: Performance
- **Measurement Method**: API latency benchmarks.
- **Acceptance Criteria**: Average recommendation request latency < 150ms.
- **Negative Cases**: Responses should not hang or timeout.
- **Related Tests**: `test_full_project_regression.py`
- **Status**: Implemented

---

### NFR-08: Maintainability
- **Name**: Coding Style Compliance
- **Description**: Source files obey standardized linting rules and length restrictions.
- **Quality Attribute**: Maintainability
- **Measurement Method**: Ruff compliance checks.
- **Acceptance Criteria**: Zero styling or quality errors under `ruff check`.
- **Negative Cases**: Execution flags error if lines exceed 100-character limits.
- **Related Tests**: `pre_deploy_check.py`
- **Status**: Implemented

---

### NFR-09: Testability
- **Name**: Unit Test Coverage
- **Description**: Validates that all agents, routes, repositories, and helper tools pass automated test checks.
- **Quality Attribute**: Testability
- **Measurement Method**: Pytest execution.
- **Acceptance Criteria**: 100% success rate across test suites.
- **Negative Cases**: Fails CI workflow if a single unit test collapses.
- **Related Tests**: `test_ci_workflows.py`
- **Status**: Implemented

---

### NFR-10: Observability
- **Name**: Trace Logging
- **Description**: Assigns transaction tracing metrics to debug requests without writing payload bodies.
- **Quality Attribute**: Maintainability / Observability
- **Measurement Method**: Log parser validations checking request formats.
- **Acceptance Criteria**: Logs request ids and routes; excludes body contents.
- **Negative Cases**: Verification fails if payload bodies are detected in console logs.
- **Related Tests**: `test_observability.py`
- **Status**: Implemented

---

### NFR-11: Compatibility
- **Name**: API version routing
- **Description**: Version path routes align with legacy configurations to avoid breaking client compatibility.
- **Quality Attribute**: Portability / Extensibility
- **Measurement Method**: Regression API calls.
- **Acceptance Criteria**: Root and versioned api paths respond to request schemas.
- **Negative Cases**: Returns HTTP 404 only on non-existent endpoints.
- **Related Tests**: `test_api_versioning.py`
- **Status**: Implemented

---

### NFR-12: Portability / Docker Runtime
- **Name**: Containerization Portability
- **Description**: Packages runtime dependencies to compile successfully under Docker.
- **Quality Attribute**: Portability
- **Measurement Method**: Docker container checks.
- **Acceptance Criteria**: Image compiles successfully; health checks pass.
- **Negative Cases**: Build fails if target runtime environment is missing.
- **Related Tests**: `docker_smoke_check.py`
- **Status**: Implemented

---

### NFR-13: Documentation Quality
- **Name**: Docs Consistency checks
- **Description**: Ensures design files and setup guides remain up-to-date and free from invalid claims.
- **Quality Attribute**: Maintainability
- **Measurement Method**: Automated consistency audits.
- **Acceptance Criteria**: Document audit validator reports PASS.
- **Negative Cases**: Returns FAIL if claims of full postgresql/auth are found.
- **Related Tests**: `test_documentation.py`
- **Status**: Implemented

---

### NFR-14: CI/CD Quality Gates
- **Name**: Continuous Integration Validation
- **Description**: Blocks merging changes if styling, tests, or security scans fail.
- **Quality Attribute**: Portability / Maintainability
- **Measurement Method**: GitHub Actions execution.
- **Acceptance Criteria**: Automatic triggers on push/pull requests report successful checks.
- **Negative Cases**: Fails workflows if quality criteria are unmet.
- **Related Tests**: `test_ci_workflows.py`
- **Status**: Implemented

---

### NFR-15: Deployment Readiness
- **Name**: Deployment Runbooks and rollback preparation
- **Description**: Provides standard operations checkbooks to safely deploy and revert containers.
- **Quality Attribute**: Operational Readiness
- **Measurement Method**: Audit checklist tests.
- **Acceptance Criteria**: Detailed rollback guidelines exist and pre-deploy validations pass.
- **Negative Cases**: Verification fails if checklist documents are missing.
- **Related Tests**: `test_deployment_docs.py`
- **Status**: Implemented
