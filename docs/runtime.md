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
