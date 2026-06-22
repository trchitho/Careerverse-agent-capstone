# Known Limitations

This document lists the technical boundaries and non-goals of the current CareerVerse Agent MVP.

### 1. Static Local Dataset
All careers, skills, and roadmaps are mapped out in static JSON templates:
- `careers.json`
- `skills.json`
- `roadmaps.json`

The system does not scrape live job sites or dynamically query external career boards.

### 2. Deterministic Matching Engine
Matches are ranked using a Jaccard similarity scoring formula based on keyword overlap. The system does not use AI neural network models or vector embeddings by default.

### 3. No Production Database
The system does not utilize a SQL/NoSQL database (e.g. PostgreSQL, Neo4j). All user configuration records and saved recommendation sessions reside in temporary RAM cache and clear when the server processes restart.

### 4. No Production Authentication
The application does not enforce password protection, JWT tokens, OAuth, or user account registrations. Session separation relies on client-generated Session IDs.

### 5. Ephemeral Feedback Storage
Feedback ratings and sanitized comments are collected in a local mock repository. Records are lost when the container or server process restarts.

### 6. External LLM Disabled by Default
Generative fit explanations via Google Gemini are optional and disabled by default. If enabled, it requires manual provisioning of a `GOOGLE_API_KEY` through environment variables.

### 7. No Public Deployment
The application is designed to run in local Docker container runtimes. There is no official, publicly hosted Web URL configured.

### 8. Guidance Nature Only
The matcher serves educational goals only:
- It does not guarantee employment outcomes or career transitions.
- It does not perform clinical psychological evaluations or official aptitude testing.
