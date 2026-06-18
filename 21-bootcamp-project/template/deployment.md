# Deployment Guide

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | `brew install python@3.12` or [python.org](https://python.org) |
| Docker | 24+ | [docker.com](https://docker.com) |
| Docker Compose | v2+ | Bundled with Docker Desktop |
| Git | 2.30+ | `brew install git` |
| Cloud CLI | — | See [Cloud Provider](#cloud-provider-setup) below |

## Environment Setup

### 1. Clone and Install

```bash
git clone <repo-url>
cd <project-directory>
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

```bash
# Required
API_KEY=your-api-key-here
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0

# Model
MODEL_NAME=your-model-name
LLM_API_KEY=your-llm-api-key
VECTOR_DB_URL=http://localhost:6333

# Deployment
ENVIRONMENT=development
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000
```

### 3. Start Dependencies

```bash
docker compose up -d postgres redis qdrant
```

Verify services are running:

```bash
docker compose ps
```

## Docker Setup

### Dockerfile

```dockerfile
FROM python:3.12-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e "."

# Copy application code
COPY src/ src/
COPY models/ models/

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - postgres
      - redis
      - qdrant
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: changeme
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  pgdata:
  qdrant_data:
```

### Build and Run

```bash
# Build image
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f api

# Stop
docker compose down
```

## Cloud Provider Setup

### AWS (ECS / EC2)

```bash
# Install AWS CLI
brew install awscli

# Configure
aws configure
```

**Option A: ECS Fargate (recommended)**

1. Push image to ECR:
```bash
aws ecr create-repository --repository-name ai-project
aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
docker tag ai-project:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ai-project:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-project:latest
```

2. Create ECS cluster, task definition, and service via AWS Console or CLI.

3. Set up ALB for HTTPS routing.

**Option B: EC2**

1. Launch EC2 instance (t3.medium or g4dn.xlarge for GPU).
2. Install Docker on instance.
3. Pull and run container.

### GCP (Cloud Run / Compute Engine)

```bash
# Install gcloud CLI
brew install google-cloud-sdk

# Authenticate
gcloud auth login

# Deploy to Cloud Run
gcloud run deploy ai-project \
    --image gcr.io/<project-id>/ai-project \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Azure (Container Apps / AKS)

```bash
# Install Azure CLI
brew install azure-cli

# Login
az login

# Deploy to Container Apps
az containerapp up \
    --name ai-project \
    --resource-group <rg-name> \
    --image <registry>/ai-project:latest \
    --target-port 8000
```

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `API_KEY` | Yes | API authentication key | `sk-abc123...` |
| `DATABASE_URL` | Yes | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Yes | Redis connection string | `redis://host:6379/0` |
| `MODEL_NAME` | Yes | Model identifier | `gpt-4`, `./models/model.pt` |
| `LLM_API_KEY` | Conditional | API key for LLM provider | `sk-...` |
| `VECTOR_DB_URL` | Yes | Vector database URL | `http://localhost:6333` |
| `ENVIRONMENT` | No | Environment name | `development`, `staging`, `production` |
| `LOG_LEVEL` | No | Logging level | `debug`, `info`, `warning`, `error` |
| `CORS_ORIGINS` | No | Allowed origins | `http://localhost:3000` |
| `SENTRY_DSN` | No | Sentry error tracking DSN | `https://...@sentry.io/...` |

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to [your platform]
        run: |
          # Add your deployment commands here
          echo "Deploying..."
```

## Post-Deployment Verification

```bash
# Health check
curl https://[your-url]/health

# Test prediction
curl -X POST https://[your-url]/v1/predict \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "test input"}'

# Check metrics
curl https://[your-url]/v1/metrics \
  -H "Authorization: Bearer $API_KEY"
```

## Rollback

If issues are detected after deployment:

```bash
# Docker Compose: revert to previous image
docker compose down
docker compose up -d api --no-build

# ECS: update service to previous task definition
aws ecs update-service --cluster <cluster> --service <service> --task-definition <previous-task-def>

# Cloud Run: redeploy previous revision
gcloud run services update-traffic ai-project --to-revisions=<previous-revision>=100
```

## Monitoring Setup

1. Verify metrics endpoint is responding
2. Confirm Grafana dashboards are populated (if using)
3. Test alert rules fire correctly
4. Check log aggregation is working
