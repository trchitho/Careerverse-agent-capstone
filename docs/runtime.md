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
