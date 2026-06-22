# Architecture

This document describes the component design, agent orchestration workflows, and data structures of the CareerVerse Agent system.

---

## 1. Overview
CareerVerse Agent is a deterministic multi-agent backend MVP designed for the **Agents for Good** capstone track. It ingests student profile data, performs explainable scoring, maps skill gaps, and returns personalized learning roadmaps. It is implemented in Python using FastAPI, Pydantic, and local JSON datasets, providing a zero-cost, private, and highly testable workflow for the Kaggle Capstone.

---

## 2. Design Goals
- **Zero-Cost & Offline**: Operates fully locally without external API keys or cloud database dependencies.
- **Privacy & Safety First**: Uses a Zero-Trust Safety Layer to block prompt injections and scrub sensitive identifiers.
- **Explainability**: Replaces black-box recommendation models with a deterministic, rule-based scoring engine.
- **Standards Aligned**: Follows the Model Context Protocol (MCP) design pattern for tool-based resource exposure.

---

## 3. System Context
The backend acts as a service layer that ingests user profiles and outputs recommendation objects. It is designed to expose both standard REST APIs and an MCP-style tool server interface, allowing external LLM orchestration runtimes or frontend clients to inspect its capabilities and query its datasets.

---

## 4. Component Architecture

```mermaid
flowchart TD
    subgraph Client Layer
        Web[React Web UI Client]
    end

    subgraph FastAPI API Layer
        API[app.main:app]
        ReqID[Request ID Middleware]
        
        Web -->|HTTP Requests| ReqID
        ReqID --> API
        
        API --> Health[Health: /api/v1/health/live | ready]
        API --> Meta[Metadata: /api/v1/metadata]
        API --> Val[Profile: /api/v1/profiles/validate]
        API --> Rec[Recommend: /api/v1/recommend]
        API --> Feed[Feedback: /api/v1/feedback/*]
        API --> Metrics[Metrics: /api/v1/metrics/summary]
        API --> MCP[MCP Routes: /api/v1/mcp/*]
    end

    subgraph Safety & Validation Layer
        Val --> Pyd[Pydantic Profile Schemas]
        Rec --> Safe[Safety Layer: detect_prompt_injection]
        Feed --> FdSafe[Comment Sanitizer & Filter]
    end

    subgraph Multi-Agent Orchestration Layer
        Safe --> AdvAgent[CareerAdvisorAgent]
        AdvAgent --> Engine[Career Scoring Engine]
        AdvAgent --> SkillAgent[SkillGapAgent]
        AdvAgent --> RoadAgent[RoadmapAgent]
    end

    subgraph Data & MCP Tool Layer
        Engine --> Tools[career_tools.py]
        SkillAgent --> Tools
        RoadAgent --> Tools
        Tools --> Careers[(app/data/careers.json)]
        Tools --> Skills[(app/data/skills.json)]
        Tools --> Roadmaps[(app/data/roadmaps.json)]
        MCP --> Tools
    end
    
    subgraph Feedback & Metrics Store
        FdSafe --> FdRepo[(InMemoryFeedbackRepository)]
        Metrics --> FdRepo
    end
```

---

## 5. Multi-Agent Workflow
Orchestrated by the `CareerAdvisorAgent`, the system runs a sequential execution pattern:
1. **Validation & Filter**: The input is run through safety checkers. If passed, the profile is forwarded.
2. **Recommendation Scoring**: The agent calls the **Career Scoring Engine** to match interest, skills, and goals against the career catalog.
3. **Skill Gap Resolution**: For the top recommended career, the `SkillGapAgent` analyzes missing requirements.
4. **Roadmap Gathering**: The `RoadmapAgent` compiles a matching 30-day and 8-week structured study roadmap.
5. **Output Synthesis**: The Advisor compiles these blocks into the final `AgentRecommendationResponse` schema.

---

## 6. Career Scoring Engine
Matches user profiles against 80 local career definitions using a deterministic formula:
$$\text{Total Score} = (0.35 \times \text{Interest Match}) + (0.45 \times \text{Skill Match}) + (0.20 \times \text{Goal Match})$$
- **Interest Match**: Jaccard similarity between student interests and career tags.
- **Skill Match**: Proportion of a career's required skills that the user already possesses.
- **Goal Match**: Text similarity check searching for career keywords in the user's career goal.

---

## 7. Skill Gap Analysis
The `SkillGapAgent` compares the user's normalized skill list against the target career's required list. It produces:
- **Matched Skills**: Skills present in both lists.
- **Missing Skills**: Required skills missing from the user's profile.
- **Readiness Score**: Percentage of target skills already mastered.

---

## 8. Roadmap Generation
The `RoadmapAgent` queries `app/data/roadmaps.json` to extract detailed learning paths. It returns a personalized plan structured by:
- **30-Day Checklist**: Daily actionable study topics.
- **8-Week Project Plan**: Weekly target milestones and project briefs, matched with the user's preferred learning style and weekly hour budget.

---

## 9. MCP-Style Tool Server
Exposes tools through standard API endpoints (`/tools`, `/mcp/careers`, etc.). It acts as a local prototype for the Model Context Protocol, enabling external agents to query career catalogs, search skill descriptions, and inspect available study templates.

---

## 10. Safety Layer
Performs runtime defensive filtering:
- **Injection Detection**: Checks profile free text for override commands like *"ignore previous instructions"* or *"ignore system prompt"*.
- **Secret Redaction**: Scrubs strings matching API keys, passwords, or tokens.
- **Disclaimer Enforcement**: Appends a mandatory educational disclaimer to all recommendations.

---

## 11. Local Evaluation Pipeline
An offline regression test runner (`app/evals/evaluate_agent.py`) that loads a test set of 14 profiles (7 normal, 4 edge cases, 1 injection attack, 2 invalid schemas). It verifies contract outputs and scoring bounds, returning exit code `0` on success or `1` on failure.

---

## 12. Data Layer
The data layer decouples storage via protocol repository interfaces (defined in `interfaces.py`). By default, data operations fall back to three local JSON datasets:
- [careers.json](file:///E:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/data/careers.json): 80 tech profile definitions.
- [skills.json](file:///E:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/data/skills.json): 260 detailed skill tags and aliases.
- [roadmaps.json](file:///E:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/data/roadmaps.json): 80 pre-mapped learning paths.
Ephemeral recommendation snapshots are managed by an in-memory session repository.

---

## 13. API Layer
Built on FastAPI, the server runs completely asynchronously. It features a central router hierarchy:
- **Legacy Layer**: Direct endpoints bound to root (e.g., `/recommend`, `/metadata`, `/tools`, `/mcp/*`) to maintain full backward compatibility with older clients.
- **Versioned Layer (`/api/v1`)**: Stabilized routes organized in [app/api/v1/](file:///e:/OneDrive/Desktop/careerverse-agent-capstone/Careerverse-agent-capstone/app/api/v1) for new integrations.
- **Saved Recommendations Endpoints**: Exposes versioned endpoints `/api/v1/recommendations/save` and `/api/v1/recommendations/saved/{session_id}` to store and list recommendation summaries.
- **Unified Error Contract**: Intercepts application-level errors (like `UnsafeProfileError`, `ResourceNotFoundError`) and validation errors (`RequestValidationError`) on versioned endpoints, formatting them under a standardized `ErrorResponse` model (Pydantic schemas) to avoid exposing framework stack traces or raw malicious inputs.
- **Request Tracking & Logging**: Uses custom request tracking middleware (`X-Request-ID`) and a structured log formatter to capture execution health without recording sensitive fields or payloads.
- **Feedback Store**: Implements the `InMemoryFeedbackRepository` to collect user ratings and comments temporarily for local quality checks.

---

## 14. Implemented vs Future Architecture

> [!IMPORTANT]
> **This project uses local JSON datasets for the Kaggle MVP instead of a production database.** There is no real database connection (such as PostgreSQL, pgvector, or Neo4j) configured in the current version. Feedback is stored ephemerally in RAM.

| Feature Area | Current Implemented MVP | Future Production Roadmap |
|---|---|---|
| **Database** | Offline JSON templates (`app/data/`) & ephemerally stored RAM feedback | PostgreSQL with `pgvector` & Neo4j graph db |
| **Model Integration** | Deterministic score engine & templates | Live Gemini API orchestration layer via Google GenAI SDK |
| **MCP Interface** | FastAPI REST endpoints mimicking MCP | Standard MCP Server SDK with stdio/SSE transports |
| **Authentication** | None (Zero-Trust Input Validation & local session ID tokens) | OAuth2, JWT tokens, and RBAC admin roles |
| **Frontend** | React + TypeScript + Vite Dashboard & Swagger UI | Next.js visual dashboard, CV parser, and speech client |
| **Observability** | Structured console/file logging, `X-Request-ID` tracking, liveness/readiness health routes | Centralized logging/tracing warehouse (e.g. Sentry/OpenTelemetry) |
| **Deployment** | Local hosting (`uvicorn`) & Docker runtime | Dockerized container deployable to GCP Cloud Run / Kubernetes |
