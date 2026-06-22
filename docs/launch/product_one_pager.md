# CareerVerse Agent Product One-Pager

## Product Summary
CareerVerse Agent is a serverless multi-agent educational assistant designed to guide tech students and early-career learners through career paths matching their skills and timeline constraints.

## Target Users
- Computer Science and IT students mapping study timelines.
- Self-taught developers looking to identify technical skill gaps.
- Career changers transitioning into software engineering or data analysis.

## Problem
Generic career suggestions are often static, high-level, and disconnected from the concrete steps required to bridge competency gaps. Students struggle to identify which technical paths fit their constraints or how to acquire those skills step-by-step.

## Solution
CareerVerse Agent coordinates multiple specialized local agents to perform deterministic profile scoring, evaluate skill readiness, and synthesize structured learning roadmaps. It displays recommendations interactively on a responsive Web dashboard, incorporating strict safety checks.

## Core Features
- **Profile Matching**: Scores and ranks 80 tech careers based on interest, goal, and skill similarity.
- **Skill Gap Auditing**: Derives master/missing technical capabilities and computes readiness scores.
- **Roadmap Curriculum**: Generates actionable 30-day and 8-week plans matching the student's time budget.
- **Feedback Collection**: soliciting rating metrics and comment logs.

## What Makes It Agentic
The application decouples coordinating and executing tasks across specialized worker profiles:
- **CareerAdvisorAgent** acts as the central coordinator, validating input security before delegating work.
- **SkillGapAgent** analyzes required skills datasets to isolate missing keywords.
- **RoadmapAgent** pulls curriculum maps matching study styles and weekly time allocations.

## Safety and Responsible AI
- **Strict Disclaimers**: Clarifies that output recommendations are for educational guidance only.
- **Input Sanitization**: Rejects malicious overrides (prompt injections) and redacts email/token logs.
- **Privacy Preservation**: Minimal data design avoiding collecting contact info or storing PII.

## Technical Foundation
- **Backend**: FastAPI, Pydantic v2, Python 3.11+.
- **Frontend**: React 18, TypeScript, Vite, custom responsive CSS.
- **Data access**: Protocol repository layers pulling from local JSON files.

## Demo Flow
1. User enters skills and goals on the React Web Client.
2. Safety middleware validates input integrity.
3. Matching results load, showing progress bars and detailed curriculums.
4. User submits anonymous feedback.

## Current Limitations
- **No Deployed Public URL**: The app is designed for local container runtimes.
- **Deterministic Scorer**: The match engine is rule-based and does not synthesize original text.
- **Ephemeral Store**: All feedback and session recommendation records reside in process RAM.
- **No Job Placement**: It does not guarantee employment outcomes or represent a hiring agency.
- **No Clinical Assessments**: It does not replace professional counseling or clinical psychological evaluations.

## Future Roadmap
- Integration of Google GenAI SDK for personalized fit explanations.
- pgvector support for semantic search indexing.
- PDF/Word CV parser to populate profiles automatically.
