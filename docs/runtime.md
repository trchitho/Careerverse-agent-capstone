# Runtime Guide

## Overview
This guide documents the execution environments for the CareerVerse Agent system. The application is designed to run locally, within a Docker container, and via Docker Compose. The default runtime does not require external API keys.

## Local Runtime
To run the application locally outside of containers:

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the API server:
   ```bash
   uvicorn app.main:app --reload
   ```
   Or bind to all interfaces:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Docker Runtime
To build the Docker image:
```bash
docker build -t careerverse-agent-api .
```

To run the container standalone:
```bash
docker run --rm -p 8000:8000 careerverse-agent-api
```

## Docker Compose Runtime
To spin up the service in Docker Compose:
```bash
docker compose up --build
```

## Environment Variables
The application reads settings from environment variables. Do not commit .env files or real secrets.
- `ENVIRONMENT`: Env stage (`production`, `development`).
- `MODEL_NAME`: Underlying engine name.
- `ENABLE_LLM_EXPLANATIONS`: Boolean flag.
- `GOOGLE_API_KEY`: Optional key placeholder.

## Health Checks
The FastAPI app contains a health check endpoint at `GET /` which returns the service health status. The Docker container executes health check checks using urllib.

## Readiness Checks
Readiness checks can query `GET /metadata` and `GET /tools` to verify availability of loaded skills and dataset capabilities.

## Dataset Availability
The system does not connect to external databases by default. High-fidelity career guidance data (careers, skills, roadmaps) is loaded locally from JSON datasets during service startup.

## Safety Runtime Rules
All input profiles are validated by the Zero-Trust safety layer. Prompt injections are automatically blocked (HTTP 400), and sensitive tokens are scrubbed. Recommendation payloads include educational safety disclaimers.

## Common Commands
- `pytest` to run tests.
- `python scripts/docker_smoke_check.py` to run Docker test build.

## Troubleshooting
If a container fails to start, verify port 8000 is not in use or check docker-compose environment configurations.

## Production Notes
This application is an offline Capstone MVP. Production deployments would require adding OAuth2 authentication, rate limiting, and persistent databases.
