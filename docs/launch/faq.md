# FAQ - Frequently Asked Questions

This document provides answers to common questions about the design, safety, and limitations of the CareerVerse Agent.

### What is CareerVerse Agent?
It is a multi-agent educational assistant designed to help tech students explore career paths, evaluate skill gaps, and preview structured learning timelines.

### Is this a real hiring platform?
No. CareerVerse is an educational guidance tool for early-career exploration. It is not associated with hiring agencies, placement services, or technical headhunters.

### Does it guarantee a job?
No. All suggestions, timelines, and roadmaps are for learning guidance only. The system does not guarantee employment, internship matches, or recruiting outcomes.

### Does it replace a counselor?
No. The recommendations are based on deterministic scoring metrics and should supplement, not replace, professional academic or career counseling.

### Does it use real Gemini by default?
No. The Gemini explanation layer is optional and disabled by default. The system operates fully offline using predefined explanation templates to avoid external dependencies.

### Does it store my private data?
No. The system implements a data-minimization design. It does not store user profiles, passwords, emails, or personal identification details. All saved snapshots and feedback logs are stored ephemerally in process RAM.

### Why are recommendations deterministic?
Deterministic scoring ensures explainability and auditability. The system uses Jaccard similarity algorithms to rank technical paths, ensuring suggestions are repeatable and transparent.

### How do I run it locally?
1. Start backend: `uvicorn app.main:app --reload`
2. Start web frontend: `cd web && npm run dev`
3. Open browser: `http://localhost:5173`

### How do I test it?
Run the pre-deployment script:
```bash
python scripts/pre_deploy_check.py
```
This executes lints, compile checks, evaluation pipelines, and pytest suites.

### What are future improvements?
Future work includes integrating live job vacancy scrapers, PostgreSQL database connection, vector-based semantic retrieval, and real Google Gemini LLM API configurations.
