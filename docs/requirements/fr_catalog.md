# Functional Requirements (FR) Catalog

This catalog outlines the Functional Requirements for the CareerVerse Agent system.

---

### FR-01: Health and Metadata
- **Name**: Health and Metadata APIs
- **Description**: Exposes system liveness/readiness indicators and metadata statistics.
- **Implemented Components**: [health.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1/health.py)
- **Endpoints**: `GET /`, `GET /metadata`, `GET /api/v1/health/live`, `GET /api/v1/health/ready`
- **Expected Behavior**: Returns HTTP 200 with JSON payload containing status, dataset sizes, and startup metrics.
- **Negative Cases**: Returns HTTP 503 Service Unavailable if datasets are corrupted or missing.
- **Related Tests**: `test_health.py`
- **Status**: Implemented

---

### FR-02: Profile Validation
- **Name**: User Career Profile Validation
- **Description**: Validates that incoming user profiles (interests, skills, and goals) match constraints.
- **Implemented Components**: [profile_schema.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/schemas/profile_schema.py)
- **Endpoints**: `POST /profiles/validate`
- **Expected Behavior**: Returns validated profile structure if input fields satisfy boundaries.
- **Negative Cases**: Returns HTTP 422 Unprocessable Entity if name, interests, skills, or goal are empty.
- **Related Tests**: `test_profile_validation_api.py`
- **Status**: Implemented

---

### FR-03: Career Recommendation
- **Name**: Career Recommendation Engine
- **Description**: Recommends top matching careers for a student profile.
- **Implemented Components**: [recommend.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1/recommend.py)
- **Endpoints**: `POST /recommend`, `POST /api/v1/recommend`
- **Expected Behavior**: Returns ranked career recommendations with match percentages.
- **Negative Cases**: Returns HTTP 400 Bad Request if fields trigger security overrides.
- **Related Tests**: `test_recommend_api.py`
- **Status**: Implemented

---

### FR-04: Scoring Engine
- **Name**: Deterministic Career Scorer
- **Description**: Computes Jaccard similarity scoring based on interest, skills, and goal overlaps.
- **Implemented Components**: [career_scorer.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/core/career_scorer.py)
- **Endpoints**: Internal scoring module
- **Expected Behavior**: Accurately matches profile attributes to catalog templates.
- **Negative Cases**: Default to 0.0 scores if no overlaps exist.
- **Related Tests**: `test_career_tools.py`
- **Status**: Implemented

---

### FR-05: Multi-Agent Orchestration
- **Name**: Multi-Agent Execution Lifecycle
- **Description**: Sequentially invokes advisor, skill gap, and roadmap workers to build output.
- **Implemented Components**: [coordinator.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/agents/coordinator.py)
- **Endpoints**: Internal orchestration pipeline
- **Expected Behavior**: Successive flow from validation, evaluation, to curriculum mapping.
- **Negative Cases**: Gracefully report agent errors if a worker fails.
- **Related Tests**: `test_agent_workflow.py`
- **Status**: Implemented

---

### FR-06: Skill Gap Analysis
- **Name**: Skill Gap Evaluator
- **Description**: Isolates missing capabilities and computes a learner's readiness percentage.
- **Implemented Components**: [skill_gap_agent.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/agents/skill_gap_agent.py)
- **Endpoints**: Internal worker module
- **Expected Behavior**: Identifies exact missing keywords from career pre-requisites.
- **Negative Cases**: Graceful fallback to empty gaps if all skills are possessed.
- **Related Tests**: `test_skill_gap_agent.py`
- **Status**: Implemented

---

### FR-07: Roadmap Generation
- **Name**: Personalized Study Curriculum
- **Description**: Synthesizes 30-day and 8-week task timelines.
- **Implemented Components**: [roadmap_agent.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/agents/roadmap_agent.py)
- **Endpoints**: Internal worker module
- **Expected Behavior**: Adjusts roadmap depth based on weekly study time allocation.
- **Negative Cases**: Default templates if profile goal matches no target career roadmap.
- **Related Tests**: `test_roadmap_agent.py`
- **Status**: Implemented

---

### FR-08: Safety and Prompt Injection Blocking
- **Name**: Payload Security Interceptor
- **Description**: Blocks prompt injections and system rule overrides.
- **Implemented Components**: [safety_tools.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/tools/safety_tools.py)
- **Endpoints**: Shared safety layer middleware
- **Expected Behavior**: Raises HTTP 400 Bad Request on inject triggers.
- **Negative Cases**: Rejects empty payloads or extreme length injection strings.
- **Related Tests**: `test_safety_tools.py`
- **Status**: Implemented

---

### FR-09: Sensitive Data Redaction
- **Name**: Log and Payload Scrubber
- **Description**: Scrubs credentials and PII like email formats.
- **Implemented Components**: [safety_tools.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/tools/safety_tools.py)
- **Endpoints**: Log filtering and comments sanitization
- **Expected Behavior**: Replaces matches with `[Redacted due to input safety warning]`.
- **Negative Cases**: Retains normal content when no PII pattern matches.
- **Related Tests**: `test_safety.py`
- **Status**: Implemented

---

### FR-10: MCP Tool Catalog
- **Name**: MCP Tool Discovery List
- **Description**: Lists mock Model Context Protocol catalog endpoints.
- **Implemented Components**: [mcp.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1/mcp.py)
- **Endpoints**: `GET /tools`, `GET /api/v1/tools`
- **Expected Behavior**: Returns listing of discovery tools and resources.
- **Negative Cases**: Empty list if server tools configurations fail.
- **Related Tests**: `test_mcp_api.py`
- **Status**: Implemented

---

### FR-11: MCP Career Resource Access
- **Name**: MCP Career Loader
- **Description**: Permits mock client fetching of target career profiles.
- **Implemented Components**: [mcp.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1/mcp.py)
- **Endpoints**: `GET /mcp/careers`
- **Expected Behavior**: Exposes careers lists asynchronously.
- **Negative Cases**: Returns HTTP 404 if requested resource template doesn't exist.
- **Related Tests**: `test_mcp_server.py`
- **Status**: Implemented

---

### FR-12: MCP Skill Resource Access
- **Name**: MCP Skill Loader
- **Description**: Permits mock client fetching of skill keyword mappings.
- **Implemented Components**: [mcp.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1/mcp.py)
- **Endpoints**: `GET /mcp/skills`
- **Expected Behavior**: Exposes skill listings.
- **Negative Cases**: Safe empty response if skill index files are unavailable.
- **Related Tests**: `test_mcp_server.py`
- **Status**: Implemented

---

### FR-13: API Versioning and Legacy Compatibility
- **Name**: Router Versioning Wrapper
- **Description**: Version paths through `/api/v1` prefixes while preserving root routes.
- **Implemented Components**: [main.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/main.py)
- **Endpoints**: `GET /`, `POST /recommend`, `/api/v1/recommend`
- **Expected Behavior**: Invokes same recommend engine across root and versioned endpoints.
- **Negative Cases**: Handled uniformly through standardized error routers.
- **Related Tests**: `test_api_versioning.py`
- **Status**: Implemented

---

### FR-14: Error Contract and Safe Errors
- **Name**: JSON Schema Error Contract
- **Description**: Wraps validation and execution errors into descriptive JSON contracts.
- **Implemented Components**: [main.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/main.py)
- **Endpoints**: Global error boundary
- **Expected Behavior**: Returns `{"detail": [{"loc": [...], "msg": "...", "type": "..."}]}`.
- **Negative Cases**: Prevents leaking private tracebacks on internal runtime errors.
- **Related Tests**: `test_error_contract.py`
- **Status**: Implemented

---

### FR-15: Repository JSON Data Access
- **Name**: Persistence Abstraction Layer
- **Description**: Reads profile templates and career files via decoupled repositories.
- **Implemented Components**: [career_repository.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/repositories/career_repository.py)
- **Endpoints**: Internal repository interfaces
- **Expected Behavior**: Correctly reads JSON files at startup and provides structured dataclasses.
- **Negative Cases**: Raises validation exceptions if JSON data is malformed.
- **Related Tests**: `test_repositories.py`
- **Status**: Implemented

---

### FR-16: Optional Explanation Service Offline Fallback
- **Name**: Explanations Fallback
- **Description**: Falls back to offline heuristic reasons if Google GenAI API is unconfigured.
- **Implemented Components**: [explanation_service.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/services/explanation_service.py)
- **Endpoints**: Internal service layer
- **Expected Behavior**: Serves deterministic summaries instantly without requesting keys.
- **Negative Cases**: Returns default safety disclaimers if fallback fails.
- **Related Tests**: `test_explanation_service.py`
- **Status**: Implemented

---

### FR-17: Saved Recommendations Session-Safe Storage
- **Name**: Ephemeral Session Recommendations
- **Description**: Stores saved recommendation matches on client-generated Session IDs.
- **Implemented Components**: [saved_recommendations.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1/saved_recommendations.py)
- **Endpoints**: `POST /api/v1/saved-recommendations`, `GET /api/v1/saved-recommendations`
- **Expected Behavior**: Correctly stores and retrieves recommendation reports.
- **Negative Cases**: Excludes personal PII metadata.
- **Related Tests**: `test_saved_recommendations.py`
- **Status**: Implemented

---

### FR-18: Feedback Submission
- **Name**: Anonymous Rating Submissions
- **Description**: Receives user ratings and sanitizes comment strings.
- **Implemented Components**: [feedback.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1/feedback.py)
- **Endpoints**: `POST /api/v1/feedback/recommendation`
- **Expected Behavior**: Records feedback comments safely (max 300 chars, whitespace trimmed).
- **Negative Cases**: Filters prompt overrides and redacts emails from reviews.
- **Related Tests**: `test_feedback_api.py`
- **Status**: Implemented

---

### FR-19: Metrics Summary
- **Name**: Aggregated Ratings Counter
- **Description**: Exposes summary rating statistics for evaluation purposes.
- **Implemented Components**: [metrics.py](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1/metrics.py)
- **Endpoints**: `GET /api/v1/metrics/summary`
- **Expected Behavior**: Returns counts of ratings, average scores, and liveness states.
- **Negative Cases**: Safe default summary if no feedback has been submitted.
- **Related Tests**: `test_feedback_api.py`
- **Status**: Implemented

---

### FR-20: Web UI Profile Submission and Result Display
- **Name**: Frontend Integration Client
- **Description**: Frontend form submitting profile requirements and rendering recommendations dashboard.
- **Implemented Components**: [App.tsx](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/web/src/App.tsx)
- **Endpoints**: Frontend client routes
- **Expected Behavior**: Form triggers backend call and handles loading, results, roadmaps, and widgets.
- **Negative Cases**: Renders clear error messages on API communication loss.
- **Related Tests**: `test_web_structure.py`
- **Status**: Implemented
