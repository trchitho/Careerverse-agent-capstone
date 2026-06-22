# Test Strategy

This document outlines the testing strategy for the CareerVerse Agent Capstone project.

## 1. Overview
The testing strategy is designed to ensure 100% compliance across all 20 Functional Requirements (FR) and 15 Non-Functional Requirements (NFR) specified in the product catalogs. It provides a multi-layered verification harness spanning unit tests, integration tests, offline evaluation pipelines, API smoke tests, static security checks, documentation consistency validators, and automated requirements verification runners.

## 2. Scope
- **In Scope**:
  - FastAPI endpoints (legacy root and `/api/v1` routers).
  - Validation schemas, input filters, and sanitization mechanisms.
  - Multi-agent coordination workers (advisor, skill gap, roadmap agents).
  - Deterministic similarity scoring calculations.
  - Model offline evaluations with calibrated profile dataset mapping.
  - Portability (Docker, Docker Compose environments).
  - Observability (JSON structured logging, X-Request-ID trace tracing).
  - Continuous integration workflows.
  - Market launch pack and deployment runbooks compliance.
- **Out of Scope**:
  - Verification of active live third-party cloud deployments.
  - Real, paid SaaS external checking tools (SonarQube, Snyk).
  - Real Google Gemini LLM API calls requiring private active credentials in automated test runner runs.

## 3. FR Testing Strategy
Each Functional Requirement is validated via a suite of data-driven tests defined in `fr_cases.json` (at least 50 cases per FR, total 1000+ cases).
The verification runner evaluates:
- Successful processing of positive inputs.
- Safe rejection of invalid types, values, or missing variables.
- Accurate routing and structure of responses.

## 4. NFR Testing Strategy
Non-Functional Requirements are verified through programmatic checks defined in `nfr_cases.json` (at least 50 cases per NFR, total 750+ cases).
Verification checks cover:
- **Security & Privacy**: Checking git index for tracked cache files, credentials scanning.
- **Observability**: Asserting logger format and request headers.
- **Reliability & Fallbacks**: Testing system operation during mock GenAI SDK errors.
- **Determinism**: Validating evaluation score drift limits.
- **Maintainability & CI/CD**: Checking coding standards and GitHub Actions properties.

## 5. Regression Testing
Full regression is run before deployment, ensuring changes to versioning, logging, or persistency do not disrupt core functionalities. Regression suites reside in `tests/test_full_project_*_regression.py`.
