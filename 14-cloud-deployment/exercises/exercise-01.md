# Exercise 01: Containerize and Deploy an AI App

## Overview

In this exercise, you'll containerize a Python/FastAPI AI backend and deploy it to Google Cloud Run. You'll practice the complete deployment pipeline from Dockerfile to production.

**Time**: 45-60 minutes

---

## Part 1: Write a Dockerfile (15 min)

### Task

Create a Dockerfile for this Python application:

```python
# main.py
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Classifier")

class ClassifyRequest(BaseModel):
    text: str

class ClassifyResponse(BaseModel):
    label: str
    confidence: float

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/classify", response_model=ClassifyResponse)
async def classify(request: ClassifyRequest):
    # Placeholder - in real app, this calls an LLM
    return ClassifyResponse(label="positive", confidence=0.95)

@app.get("/")
async def root():
    return {"message": "AI Classifier API", "docs": "/docs"}
```

```txt
# requirements.txt
fastapi==0.115.0
uvicorn[standard]==0.30.0
pydantic==2.9.0
python-dotenv==1.0.1
```

### Requirements

Your Dockerfile must:

1. Use `python:3.11-slim` as the base image
2. Set working directory to `/app`
3. Set `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1`
4. Copy and install `requirements.txt` before copying app code
5. Expose port 8000
6. Run uvicorn with `--host 0.0.0.0`
7. Include a `HEALTHCHECK` instruction

### Deliverable

Save your Dockerfile in a new directory called `classifier-app/`.

---

## Part 2: Build and Run Locally (10 min)

### Task

Using the Dockerfile from Part 1:

1. Build the image
2. Run the container
3. Test all endpoints
4. Verify health check works

### Commands to Run

```bash
# Build the image
docker build -t classifier-app:latest .

# Run the container
docker run -d --name classifier -p 8000:8000 classifier-app:latest

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'

# View logs
docker logs classifier

# Stop and remove
docker stop classifier
docker rm classifier
```

### Verify

- [ ] Image builds without errors
- [ ] Container starts and stays running
- [ ] All three endpoints respond correctly
- [ ] Health check returns healthy status
- [ ] Container can be stopped and removed cleanly

---

## Part 3: Deploy to Google Cloud Run (15 min)

### Prerequisites

- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated
- Docker running locally

### Task

Deploy your containerized app to Google Cloud Run.

### Steps

```bash
# 1. Authenticate (if not already)
gcloud auth login

# 2. Set your project
gcloud config set project YOUR_PROJECT_ID

# 3. Enable required APIs
gcloud services enable run.googleapis.com containerregistry.googleapis.com

# 4. Deploy (choose ONE method)

# Method A: Deploy from source (recommended)
gcloud run deploy classifier-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 5

# Method B: Deploy from pre-built image
gcloud auth configure-docker
docker tag classifier-app:latest gcr.io/YOUR_PROJECT_ID/classifier-app:latest
docker push gcr.io/YOUR_PROJECT_ID/classifier-app:latest
gcloud run deploy classifier-app \
  --image gcr.io/YOUR_PROJECT_ID/classifier-app:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Verify

- [ ] Deployment completes successfully
- [ ] Service URL is accessible
- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] Classify endpoint works with POST request
- [ ] Logs are visible in GCP Console

### Test Your Deployed Service

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe classifier-app --region us-central1 --format 'value(status.url)')

# Test
curl $SERVICE_URL/health
curl -X POST $SERVICE_URL/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Deploying to Cloud Run is easy!"}'
```

---

## Part 4: Environment Variables and Secrets (10 min)

### Task

1. Add environment variable support to your app
2. Set up Secret Manager for sensitive data
3. Deploy with proper configuration

### Steps

**Step 1**: Update `main.py` to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "default")
API_KEY = os.getenv("API_KEY", "")
```

**Step 2**: Create `.env.example`:

```
MODEL_NAME=gemini-pro
API_KEY=your-api-key-here
```

**Step 3**: Create a secret in GCP:

```bash
# Create secret
echo -n "test-api-key-12345" | gcloud secrets create classifier-api-key --data-file=-

# Grant access to Cloud Run service account
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format 'value(projectNumber)')
gcloud secrets add-iam-policy-binding classifier-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

**Step 4**: Deploy with secrets:

```bash
gcloud run deploy classifier-app \
  --source . \
  --region us-central1 \
  --set-env-vars "MODEL_NAME=gemini-pro" \
  --set-secrets "API_KEY=classifier-api-key:latest" \
  --allow-unauthenticated
```

**Step 5**: Verify the environment variables are available:

```bash
# Check logs to see MODEL_NAME is set
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=classifier-app" --limit 10
```

### Verify

- [ ] App reads `MODEL_NAME` from environment
- [ ] Secret is mounted as `API_KEY`
- [ ] Secret value doesn't appear in logs or container inspection
- [ ] `.env.example` is committed (but `.env` is not)

---

## Bonus: CI/CD with GitHub Actions (15 min)

### Task

Create a GitHub Actions workflow that automatically deploys to Cloud Run on push to `main`.

### Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

env:
  PROJECT_ID: YOUR_PROJECT_ID
  SERVICE_NAME: classifier-app
  REGION: us-central1

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Auth to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/YOUR_PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
          service_account: github-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com

      - name: Deploy to Cloud Run
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: ${{ env.SERVICE_NAME }}
          region: ${{ env.REGION }}
          image: gcr.io/${{ env.PROJECT_ID }}/${{ env.SERVICE_NAME }}
```

**Note**: This requires setting up Workload Identity Federation in GCP. For simpler setup, you can use a service account key (less secure, not recommended for production).

### Verify

- [ ] Push to `main` triggers the workflow
- [ ] Deployment completes successfully
- [ ] New version is live at the service URL
- [ ] Previous revision is available for rollback

---

## Submission

Save your work in a `classifier-app/` directory with:

- `main.py` — Your FastAPI application
- `requirements.txt` — Dependencies
- `Dockerfile` — Container build instructions
- `.dockerignore` — Files to exclude
- `.env.example` — Environment variable template
- `.github/workflows/deploy.yml` — CI/CD workflow (bonus)

## Grading

| Criteria | Points |
|----------|--------|
| Dockerfile builds successfully | 25 |
| Container runs and responds to requests | 25 |
| Deployed to Cloud Run and accessible | 25 |
| Environment variables and secrets configured | 15 |
| CI/CD workflow (bonus) | 10 |
| **Total** | **100** |
