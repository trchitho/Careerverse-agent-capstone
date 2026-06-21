# CareerVerse Agent — AI Career Guidance Agent for Students

## Subtitle
A Privacy-Safe, Zero-Cost, Deterministic Multi-Agent System Bootstrapping Career recommendations for Early-Career Learners.

---

## 1. Problem
For students and early-career individuals in the tech sector, identifying an optimal career path is challenging. Generic career counseling is often static, non-personalized, and high-level. Traditional learners require deep-dive answers: What skills do I need? Where are my gaps? What projects and learning templates can help me transition? Existing AI-driven career options often rely on cloud-hosted large language models (LLMs) that present issues concerning data privacy, high subscription or token costs, API instability, and a lack of explainable recommendation scores.

---

## 2. Solution
CareerVerse Agent is a focused, offline-first backend MVP tailored for the **Agents for Good** track. It uses a high-fidelity local dataset representing 80 tech careers, 260 skills, and 80 pre-mapped learning roadmaps. A deterministic scoring engine ranks career matches based on interests, current skills, and text-based career goals. By operating fully locally with Pydantic v2 schemas and FastAPI, CareerVerse Agent operates at zero cost, requires no internet access or API keys, and guarantees deterministic outputs for reliable local evaluation.

---

## 3. Why Agents?
The career guidance workflow requires separating distinct analytical tasks:
1. **Orchestration**: Directing the query, validation, scoring, gap mapping, and roadmap synthesis.
2. **Analysis of Readiness**: Comparing student skills against target profiles to compute gap metrics.
3. **Curriculum Design**: Structuring timeline checklists, daily tasks, and weekly projects.

Instead of writing a single monolithic script, we map these duties onto a multi-agent orchestration pattern:
- `CareerAdvisorAgent` manages the end-to-end execution flow.
- `SkillGapAgent` focuses entirely on skill comparisons and gap percentages.
- `RoadmapAgent` compiles structured learning roadmaps.

This separation of concerns makes the codebase modular, testable, and directly extensible to live LLM systems.

---

## 4. Architecture
The architecture comprises a layered system context:
- **API Entrypoint**: Asynchronous FastAPI endpoints offering health checks, metadata queries, and interactive Swagger UI.
- **Safety Filter**: A defensive layer checking profile text for prompt injection commands or secret override keywords.
- **Scoring Engine**: Evaluates Jaccard interest matches, skill proportions, and goal keywords to calculate career match ratings.
- **MCP-Style Tool Server**: Exposes local datasets using REST resource routes following Model Context Protocol standards.

> [!NOTE]
> This MVP operates entirely on offline JSON datasets rather than a production relational database. This design maintains zero configuration setup for Kaggle evaluators.

---

## 5. Key Concepts Applied
- **Multi-Agent System**: Sequential agent execution that delegates tasks to specialized sub-agents.
- **MCP-Style Tool Server**: Exposes data catalogs as machine-readable tools for easy integration into wider agent runtimes.
- **Agent Skill Documentation**: Behavioral rules and contracts are documented in structured skill specs.
- **Security & Responsible AI**: Input sanitization, prompt injection detection, and educational disclaimers.
- **Local Evaluation Pipeline**: Aggregate testing of cases to measure agent performance without API keys.
- **FastAPI Deployability**: Ready to package with Docker and run in any cloud environment.

---

## 6. Implementation
The scoring engine combines three factors to compute the final career match score:
- **Interest Match (35%)**: Similary of user interests to career keywords.
- **Skill Match (45%)**: Ratio of career required skills possessed by the student.
- **Goal Match (20%)**: Match between user career goal description and target career templates.

This provides explainable results, breaking down recommendations into transparent percentages.

---

## 7. Security and Responsible AI
The system adopts a Zero-Trust approach. Student inputs are checked for prompt injections (e.g. override commands like *Ignore previous instructions*). Detected injections trigger an HTTP 400 Bad Request without leaking internal templates. The system prints a mandatory disclaimer:
*"This system provides educational career guidance only. It does not guarantee employment outcomes or replace professional counseling."*

---

## 8. Evaluation
The offline evaluation runner (`app/evals/evaluate_agent.py`) tests 14 scenarios covering:
- **Normal profiles**: IT students, backend developers, etc.
- **Edge cases**: Vietnamese goals, career changers, duplicate normalization.
- **Security cases**: Blocked injection attempts.
- **Invalid schemas**: Missing requirements.

Running the evaluation script returns:
```text
Evaluation Summary
Total: 14 | Passed: 14 | Failed: 0 | Score: 100.00%
```

---

## 9. Demo
The demo showcases FastAPI's Swagger UI running at http://127.0.0.1:8000/docs. Evaluators can call the `/recommend` endpoint with a demo student payload to see recommendations, skill gap metrics, and roadmaps. A safety demonstration highlights immediate blocking of malicious inputs.

---

## 10. Challenges and Lessons Learned
Building a deterministic MVP showed that AI agents do not require expensive LLM APIs to perform advanced tasks. High-fidelity data structures combined with rule-based scoring engines can deliver high-quality, reproducible matches. This avoids model drift, token usage costs, and safety vulnerabilities common in live LLM pipelines.

---

## 11. Future Work
While the current MVP is fully local and deterministic, future phases include:
- **LLM Reasoning**: Adding a real Gemini API explanation layer to generate custom descriptions.
- **Vector Database**: Storing datasets in `pgvector` or Neo4j to support semantic matching.
- **MCP Integration**: Transitioning the prototype tool routes to the official Model Context Protocol python SDK.
- **User Dashboard**: Creating a Next.js front-end with CV uploading and drag-and-drop roadmap progress.
