# Module 21: Bootcamp AI-Project — AI Solution for Enterprise

## Overview

This is the capstone project of the AI Engineering curriculum. Over **3 weeks**, small teams of 3–4 students build an end-to-end AI solution for a real enterprise use case, following a structured pipeline from scoping through deployment and demo.

The goal is to simulate a real-world enterprise AI engagement: understanding business requirements, designing an architecture, building a production-quality solution, deploying it, and presenting results to stakeholders.

## Real-Company Case Study Approach

Each team selects (or is assigned) a case study based on a real company scenario:

| Industry | Example Use Case | Complexity |
|----------|-----------------|------------|
| Retail | Product recommendation engine | Medium |
| Finance | Fraud detection pipeline | High |
| Healthcare | Medical document summarization | High |
| Logistics | Demand forecasting system | Medium |
| Legal | Contract analysis and extraction | High |
| Customer Support | RAG-based support chatbot | Medium |
| HR | Resume screening and ranking | Medium |
| Manufacturing | Defect detection from images | High |

Teams must define the problem from the company's perspective — including constraints, stakeholders, and success metrics.

## Team Structure

Each team has:

| Role | Responsibility |
|------|---------------|
| **Project Lead** | Coordination, stakeholder communication, final presentation |
| **ML Engineer** | Model development, training, evaluation |
| **Data/Backend Engineer** | Data pipelines, API development, infrastructure |
| **DevOps/Full-stack** | Deployment, monitoring, frontend if applicable |

Mentors are assigned per team for weekly check-ins.

## Mentoring Schedule

| Week | Session | Focus |
|------|---------|-------|
| 1 — Scoping | Mon + Thu | Problem framing, data audit, architecture review |
| 2 — Build | Mon + Thu | Code review, model evaluation, integration testing |
| 3 — Deploy | Mon + Thu | Deployment review, demo rehearsal, final feedback |

Each session: 30 min team sync + 30 min mentor office hours.

## Project Phases

### Phase 1: Scoping (Days 1–5)

- Define the business problem and stakeholders
- Identify data sources and assess availability/quality
- Set measurable success metrics (latency, accuracy, cost)
- Draft architecture and select tech stack
- **Deliverable:** `README.md`, `architecture.md`, data audit report

### Phase 2: Design (Days 6–8)

- Finalize system architecture
- Design API contracts
- Set up development environment and CI/CD scaffold
- Plan evaluation strategy
- **Deliverable:** `api-docs.md`, environment setup, test plan

### Phase 3: Build (Days 9–15)

- Implement data ingestion and preprocessing
- Develop and train models
- Build API layer and integration points
- Write unit and integration tests
- **Deliverable:** Working codebase, test suite, model artifacts

### Phase 4: Deploy (Days 16–18)

- Containerize application
- Deploy to cloud environment
- Set up monitoring and logging
- Conduct load testing and optimization
- **Deliverable:** Live deployment, `deployment.md`, monitoring dashboards

### Phase 5: Demo (Days 19–21)

- Prepare and rehearse presentation
- Record demo walkthrough
- Document lessons learned
- Submit final artifacts
- **Deliverable:** `presentation.md`, recorded demo, final codebase

## Deliverables Checklist

| # | Deliverable | Format | Due |
|---|------------|--------|-----|
| 1 | Project README | Markdown | End of Week 1 |
| 2 | Architecture doc | Markdown + Mermaid | End of Week 1 |
| 3 | API documentation | Markdown | Start of Week 2 |
| 4 | Working codebase | Git repo | End of Week 2 |
| 5 | Test suite | Automated tests | End of Week 2 |
| 6 | Deployment guide | Markdown | End of Week 3 |
| 7 | Live deployment | URL | End of Week 3 |
| 8 | Presentation slides | Markdown/PDF | Day 21 |
| 9 | Demo recording | Video (5–10 min) | Day 21 |
| 10 | Retrospective | Markdown | Day 21 |

## Evaluation Rubric

| Criterion | Weight | Excellent (5) | Good (3) | Needs Work (1) |
|-----------|--------|---------------|----------|----------------|
| **Problem Definition** | 10% | Clear business case with quantified impact | Problem defined but metrics vague | Unclear or purely academic framing |
| **Architecture** | 15% | Production-grade, scalable, well-documented | Functional but with gaps | Ad-hoc, undocumented |
| **Data Pipeline** | 15% | Robust ingestion, validation, versioning | Basic pipeline works | Manual or brittle |
| **Model Quality** | 15% | Meets metrics, evaluated rigorously, explainable | Works but limited evaluation | Minimal evaluation |
| **Code Quality** | 10% | Clean, tested, CI/CD, follows conventions | Mostly organized, some tests | Messy, no tests |
| **Deployment** | 15% | Live, monitored, with rollback capability | Deployed but basic | Local-only or broken |
| **API Design** | 10% | RESTful, documented, versioned | Functional endpoints | Poorly structured |
| **Presentation** | 10% | Clear narrative, compelling demo, handles Q&A | Decent delivery | Hard to follow |

**Passing grade:** 3.0 weighted average.

## Tools and Technologies

### Core Stack

| Layer | Recommended | Alternatives |
|-------|------------|--------------|
| Language | Python 3.10+ | — |
| ML Framework | PyTorch / HuggingFace Transformers | TensorFlow, JAX |
| LLM / GenAI | OpenAI API / vLLM / Ollama | Anthropic, local models |
| Vector DB | ChromaDB / Qdrant / Weaviate | Pinecone, Milvus |
| API | FastAPI | Flask, Django |
| Database | PostgreSQL + Redis | SQLite (dev only) |
| Container | Docker + Docker Compose | Podman |
| Cloud | AWS / GCP / Azure (free tier) | — |
| CI/CD | GitHub Actions | GitLab CI, CircleCI |
| Monitoring | Prometheus + Grafana | Datadog, CloudWatch |
| Version Control | Git + GitHub | GitLab |

### Suggested Project Structure

```
project-root/
├── README.md
├── architecture.md
├── api-docs.md
├── deployment.md
├── presentation.md
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── ...
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── ...
│   └── utils/
│       ├── __init__.py
│       └── ...
├── tests/
│   ├── test_api.py
│   ├── test_model.py
│   └── test_pipeline.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── notebooks/
│   ├── 01-exploration.ipynb
│   ├── 02-training.ipynb
│   └── 03-evaluation.ipynb
├── models/
│   └── .gitkeep
└── docs/
    └── ...
```

## Weekly Milestones

### Week 1: Scoping & Design

- [ ] Team formed and roles assigned
- [ ] Case study selected and problem statement written
- [ ] Data sources identified and audit completed
- [ ] Architecture designed and reviewed with mentor
- [ ] Tech stack finalized and repo initialized
- [ ] API contracts drafted

### Week 2: Build

- [ ] Data pipeline implemented and tested
- [ ] Model training/experimentation completed
- [ ] API endpoints implemented
- [ ] Integration between components verified
- [ ] Unit and integration tests passing
- [ ] Code reviewed by at least one teammate

### Week 3: Deploy & Demo

- [ ] Application containerized
- [ ] Deployed to cloud with HTTPS endpoint
- [ ] Monitoring and logging configured
- [ ] Load testing completed
- [ ] Presentation rehearsed
- [ ] Demo recording completed
- [ ] All documentation finalized
- [ ] Retrospective written

## Getting Started

1. Form your team (3–4 members)
2. Select or receive your case study
3. Create a new Git repository
4. Copy the `template/` directory as your starting point
5. Begin Phase 1: Scoping
6. Schedule your first mentor check-in

Good luck. Build something that solves a real problem.
