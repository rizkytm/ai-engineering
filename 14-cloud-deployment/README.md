# Module 14: Cloud Deployment & Containerization

## Overview

Shipping an AI app from your laptop to production requires more than "it works on my machine." This module covers the full deployment pipeline: containerizing Python/FastAPI apps with Docker, managing secrets, and deploying to Google Cloud Run. You'll learn why containerization is the industry standard and how to move from development to a scalable, secure production environment.

## Learning Objectives

By the end of this module, you will be able to:

- Explain the differences between development and production environments
- Build Dockerfiles for Python/FastAPI AI applications
- Manage environment variables and secrets securely
- Deploy containers to Google Cloud Run
- Set up health checks and basic monitoring
- Understand CI/CD pipelines for containerized apps

---

## 1. Development vs Production

The gap between "runs locally" and "runs reliably for users" is where most AI projects fail.

| Aspect | Development | Production |
|--------|------------|------------|
| **Environment** | Local machine, virtualenv | Containerized, cloud-managed |
| **Secrets** | `.env` file, hardcoded | Secret managers (GCP, AWS) |
| **Dependencies** | `pip install` ad hoc | Pinned `requirements.txt` |
| **Data** | Sample datasets | Live data, real users |
| **Scaling** | Single user | Concurrent users, autoscaling |
| **Monitoring** | `print()` statements | Logs, traces, alerts |
| **Networking** | `localhost` | Public URLs, load balancers |
| **Error handling** | Crashes, restart manually | Graceful degradation, retries |
| **Cost** | Free (your laptop) | Pay-per-use (cloud billing) |

### Why This Matters for AI Apps

AI applications have unique deployment challenges:
- **Large dependencies** — ML libraries (PyTorch, TensorFlow) are 1-4 GB
- **GPU requirements** — some inference needs GPU acceleration
- **Model artifacts** — model files can be hundreds of MB to several GB
- **Variable latency** — LLM API calls have unpredictable response times
- **Stateful components** — vector databases, session stores need persistence

---

## 2. Deployment Pipeline for AI Apps

A typical AI deployment pipeline:

```
Code → Build → Test → Containerize → Push to Registry → Deploy → Monitor
 │       │       │         │              │              │         │
 │       │       │         │              │              │         └─ Logs, metrics, alerts
 │       │       │         │              │              └─ Cloud Run / Kubernetes
 │       │       │         │              └─ Container Registry (GCR, ECR, Docker Hub)
 │       │       │         └─ Docker build
 │       │       └─ Unit tests, integration tests
 │       └─ Compile, lint, type-check
 └─ Git push / PR merge
```

### Key Principles

1. **Immutable containers** — never modify a running container; rebuild and redeploy
2. **12-factor app** — store config in environment variables, not code
3. **Infrastructure as Code** — define deployments in config files, not manual steps
4. **Reproducibility** — same container runs identically everywhere

---

## 3. Docker Fundamentals

### What is Docker?

Docker packages your application and all its dependencies into a standardized unit called a **container**. Unlike virtual machines, containers share the host OS kernel, making them lightweight and fast.

```
┌─────────────────────────────────────┐
│          Container                  │
│  ┌─────────────────────────────┐   │
│  │      Application Code       │   │
│  ├─────────────────────────────┤   │
│  │      Dependencies (pip)     │   │
│  ├─────────────────────────────┤   │
│  │      Python Runtime         │   │
│  └─────────────────────────────┘   │
│          OS (Linux)                │
├─────────────────────────────────────┤
│        Host OS Kernel              │
├─────────────────────────────────────┤
│        Host Machine                │
└─────────────────────────────────────┘
```

### Key Concepts

- **Image** — A read-only template with your app, dependencies, and OS layers. Think of it as a class.
- **Container** — A running instance of an image. Think of it as an object.
- **Dockerfile** — A script of instructions to build an image.
- **Registry** — A storage for images (Docker Hub, Google Container Registry).
- **Volume** — Persistent storage that survives container restarts.

---

## 4. Dockerfile Anatomy

A Dockerfile for a Python/FastAPI AI app:

```dockerfile
# 1. Base image — use specific version, not :latest
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy dependency file first (leverages Docker cache)
COPY requirements.txt .

# 6. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy application code
COPY . .

# 8. Expose the port the app runs on
EXPOSE 8000

# 9. Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Best Practices for AI App Dockerfiles

- **Use slim images** — `python:3.11-slim` instead of `python:3.11` (saves ~700 MB)
- **Layer ordering** — put rarely-changing layers (dependencies) before frequently-changing layers (code)
- **Multi-stage builds** — build in a large image, copy only what's needed to a slim runtime
- **No secrets in image** — never `COPY .env` or hardcode API keys
- **`.dockerignore`** — exclude `.git`, `__pycache__`, `.venv`, `node_modules`

---

## 5. Environment Variables & Secrets Management

### The Problem

AI apps need API keys (Gemini, Pinecone, etc.), database URLs, and config values. Hardcoding these is a security risk — if you push to GitHub, your keys are exposed.

### The Solution

| Approach | Development | Production |
|----------|------------|------------|
| `.env` file + `python-dotenv` | Good | Never |
| OS environment variables | Good | Good |
| Secret managers (GCP Secret Manager) | Overkill | Best |
| Cloud-native config (Cloud Run env vars) | N/A | Good |

### 12-Factor App Config

Store configuration in environment variables, not in code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-pro")  # default value
```

### Protecting Secrets

1. **Never commit `.env` to git** — add it to `.gitignore`
2. **Use `.env.example`** — document required variables without values
3. **Use Secret Managers in production** — GCP Secret Manager, AWS Secrets Manager
4. **Rotate keys regularly** — compromised keys should be replaced immediately

```gitignore
# .gitignore
.env
.env.local
.env.production
*.key
```

```
# .env.example (commit this)
OPENAI_API_KEY=your-key-here
PINECONE_API_KEY=your-key-here
PINECONE_INDEX=your-index
MODEL_NAME=gemini-pro
```

---

## 6. Container Registries

A container registry stores and distributes Docker images.

| Registry | Free Tier | Best For |
|----------|-----------|----------|
| Docker Hub | 1 private repo | Open-source, personal projects |
| Google Container Registry (GCR) | 5 GB | GCP deployments |
| GitHub Container Registry (GHCR) | 500 MB | GitHub-integrated workflows |
| AWS ECR | 500 MB | AWS deployments |

### Pushing to Google Container Registry

```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Tag your image
docker tag ai-app:latest gcr.io/YOUR_PROJECT_ID/ai-app:latest

# Push to registry
docker push gcr.io/YOUR_PROJECT_ID/ai-app:latest
```

---

## 7. Google Cloud Run

### What is Cloud Run?

Cloud Run is a fully managed serverless platform that runs containers. It autoscales from zero to thousands of instances and you only pay for the compute time you use.

**Why Cloud Run for AI apps?**
- No cluster management (unlike Kubernetes)
- Automatic scaling, including scale-to-zero
- Pay per request (cost-effective for variable traffic)
- Built-in load balancing and HTTPS
- Supports custom containers (not just web apps)

### Deployment Command

```bash
# Deploy from source (Dockerfile in current directory)
gcloud run deploy ai-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "MODEL_NAME=gemini-pro" \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10
```

### Configuration Options

| Flag | Purpose | Example |
|------|---------|---------|
| `--memory` | RAM allocation | `2Gi`, `4Gi` |
| `--cpu` | CPU cores | `1`, `2`, `4` |
| `--max-instances` | Scale limit | `10`, `100` |
| `--min-instances` | Keep warm instances | `1` (avoids cold starts) |
| `--allow-unauthenticated` | Public endpoint | Remove for internal-only |
| `--set-secrets` | Mount Secret Manager secrets | `KEY=secret_name:version` |
| `--set-env-vars` | Environment variables | `"KEY=value"` |
| `--concurrency` | Requests per instance | `80` (default), `1` for GPU |

### Custom Domain Setup

```bash
# Map a domain to your Cloud Run service
gcloud run domain-mappings create \
  --service ai-app \
  --domain api.yourdomain.com \
  --region us-central1

# Then configure DNS with the provided records
```

### Monitoring & Logs

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ai-app" --limit 50

# View in console
# https://console.cloud.google.com/run
```

---

## 8. Security Best Practices

### API Keys & Credentials

- **Never log API keys** — redact in logs
- **Use least-privilege access** — service accounts with minimal permissions
- **Enable audit logging** — track who accessed what
- **Use Secret Manager** — never store secrets in environment variables for sensitive data

### Container Security

- **Scan images for vulnerabilities** — `docker scout cves ai-app:latest`
- **Run as non-root user** — `USER nonroot:nonroot` in Dockerfile
- **Keep base images updated** — rebuild regularly with `docker pull python:3.11-slim`
- **Don't run with `--privileged`** — limits container escape risks

### Network Security

- **Use HTTPS** — Cloud Run provides this by default
- **Restrict ingress** — don't use `--allow-unauthenticated` for internal services
- **Rate limiting** — protect against abuse
- **Input validation** — sanitize all user inputs

---

## 9. Health Checks & Monitoring

### Health Check Endpoints

Every production service should expose health check endpoints:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    # Check dependencies (DB, model, etc.)
    return {"status": "ready"}
```

Cloud Run uses the `/health` endpoint (or configurable path) to determine if an instance should receive traffic.

### Key Metrics to Monitor

| Metric | Why It Matters |
|--------|---------------|
| **Request latency** | User experience, SLA compliance |
| **Error rate (5xx)** | Service health |
| **Cold start time** | User experience (aim < 2s) |
| **Memory usage** | OOM kills, right-sizing |
| **Token usage** | Cost tracking for LLM calls |
| **Concurrent requests** | Scaling behavior |

### Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

@app.post("/generate")
async def generate(request: GenerateRequest):
    logger.info(f"Generate request: model={request.model}, tokens={request.max_tokens}")
    try:
        result = await llm.generate(request)
        logger.info(f"Generated: tokens_used={result.usage.total_tokens}")
        return result
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        raise
```

---

## 10. Cost Management

### Cloud Run Pricing

- **CPU**: $0.00002400/vCPU-second
- **Memory**: $0.00000250/GiB-second
- **Requests**: $0.40/million requests
- **Free tier**: 240,000 vCPU-seconds, 450,000 GiB-seconds, 2 million requests/month

### Cost Optimization Tips

1. **Use `--min-instances 0`** for non-critical services (scale to zero when idle)
2. **Set `--max-instances`** to prevent runaway costs
3. **Right-size memory/CPU** — don't over-provision
4. **Use `--concurrency` wisely** — higher concurrency = fewer instances
5. **Monitor billing alerts** — set budget alerts in GCP Console

### Example Cost Estimate

A FastAPI app serving LLM requests:
- 1 vCPU, 2 GiB RAM
- 100,000 requests/month
- Average 2s processing time

**Monthly cost**: ~$10-15 (excluding LLM API costs)

---

## Exercises

- [Exercise 01: Containerize and Deploy](exercises/exercise-01.md)

## Resources

- [Resources & References](resources.md)
