# Deployment Guide

## Overview
This document provides instructions for containerizing the CareerVerse Agent API and deploying it to cloud environments.

## Primary Target: Google Cloud Run
The primary deployment path is **Google Cloud Run**, a fully managed serverless container runtime.

## Why Cloud Run?
- **Serverless Scaling**: Scales down to zero when idle, resulting in zero cost for development and testing.
- **Docker-native**: Directly executes container builds created locally or through CI pipelines.
- **Portability**: Ensures the application behavior matches the local Docker runtime.

## Prerequisites
- A Google Cloud Platform (GCP) project.
- The `gcloud` CLI installed locally and authenticated:
  ```bash
  gcloud auth login
  gcloud config set project YOUR_PROJECT_ID
  ```
- Local Docker installation.

## Environment Variables
Ensure the following configurations are set on the target environment:
- `ENVIRONMENT`: `production` or `development`.
- `DATA_SOURCE`: `json` (use default offline JSON datasets).
- `ENABLE_LLM_EXPLANATIONS`: `false` (forces offline fallback mode, avoiding external API calls).

## Docker Build
Build the container image using the project's root Dockerfile:
```bash
docker build -t careerverse-agent-api .
```

## Local Container Test
Run and test the container locally to verify it starts and processes REST requests:
```bash
docker run --rm -p 8000:8000 careerverse-agent-api
```
Query health check:
```bash
curl http://127.0.0.1:8000/api/v1/health/live
```

## Cloud Run Deployment Steps
To push and deploy the image to Cloud Run using Google Cloud Build:

1. **Submit Build to Google Container Registry / Artifact Registry**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/careerverse-agent-api:latest
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy careerverse-agent-api \
     --image gcr.io/YOUR_PROJECT_ID/careerverse-agent-api:latest \
     --region asia-southeast1 \
     --platform managed \
     --allow-unauthenticated \
     --set-env-vars ENVIRONMENT=production,ENABLE_LLM_EXPLANATIONS=false,DATA_SOURCE=json
   ```

*(Note: Replace `YOUR_PROJECT_ID` with your actual GCP Project ID).*

## Post-Deploy Verification
Ensure the service answers correctly by querying:
- Liveness: `GET /api/v1/health/live`
- Readiness: `GET /api/v1/health/ready`
- Metrics: `GET /api/v1/metrics/summary`

## Rollback Plan
If a deployment fails or exhibits regressions, perform a rollback immediately:
1. **Cloud Run Console**: Navigate to the service, select the revisions tab, choose the previous stable revision, and direct 100% of the traffic back to it.
2. **CLI Rollback**: Run the deployment command targeting the specific stable tag:
   ```bash
   gcloud run deploy careerverse-agent-api \
     --image gcr.io/YOUR_PROJECT_ID/careerverse-agent-api:PREVIOUS_STABLE_TAG \
     --region asia-southeast1
   ```

## Alternative Deployment Options
- **Railway**: Connect the GitHub repository directly and bind the start command to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- **Render**: Create a Web Service targeting the Dockerfile environment.
- **Fly.io**: Initialize with `fly launch` and configure port mapping to internal port 8000.

## Security Notes
- **Secrets Management**: If the Google Gemini integration is enabled (`ENABLE_LLM_EXPLANATIONS=true`), do not set `GOOGLE_API_KEY` as a raw environment variable. Instead, reference it via **GCP Secret Manager** and mount it into the Cloud Run revision.
- **No Tracked .env**: Ensure no `.env` file containing secrets is added to the container build context.

## What Is Not Automated
- Provisioning GCP project structures and billing setups.
- Configuring custom domain mapping or custom SSL certificates.
