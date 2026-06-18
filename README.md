# AI Engineering Learning Resources

A structured, hands-on curriculum for learning AI Engineering — from fundamentals to production deployment.

## Modules

| # | Module | Topics |
|---|--------|--------|
| 01 | [Introduction to AI Architecture](01-intro-ai-architecture/) | AI/ML/DL/GenAI landscape, roles, system architecture |
| 02 | [Python for AI](02-python-for-ai/) | Python basics, NumPy, Pandas, API requests, Git |
| 03 | [Data Engineering](03-data-engineering/) | Data pipeline, cleaning, transformation, feature engineering |
| 04 | [Applied ML](04-applied-ml/) | Supervised/unsupervised learning, model evaluation, bias |
| 05 | [Deep Learning](05-deep-learning/) | Neural networks, embeddings, Transformer basics |
| 06 | [Transformer & LLM](06-transformer-llm/) | Self-attention, tokenization, LLM inference |
| 07 | [Text Embeddings](07-text-embeddings/) | Vector representation, semantic similarity, cosine similarity |
| 08 | [Vector Databases](08-vector-databases/) | Semantic search, Pinecone, FAISS, ANN |
| 09 | [LLM Ecosystem](09-llm-ecosystem/) | Proprietary vs open-source, Hugging Face, model selection |
| 10 | [Prompt Engineering](10-prompt-engineering/) | Structured prompts, few-shot, chain-of-thought, templates |
| 11 | [RAG](11-rag/) | Retrieval-augmented generation, chunking, LangChain |
| 12 | [Orchestration & Agents](12-orchestration-agents/) | LangChain, LangGraph, tool calling, multi-step workflows |
| 13 | [AI Backend & API](13-ai-backend-api/) | FastAPI, Pydantic, LLM integration, testing |
| 14 | [Cloud Deployment](14-cloud-deployment/) | Docker, containerization, Google Cloud Run |
| 15 | [Observability](15-observability/) | LLMOps, LangSmith, tracing, cost monitoring |
| 16 | [Scaling & Optimization](16-scaling-optimization/) | Caching, batch inference, model routing, cost optimization |
| 17 | [AI-Accelerated Dev](17-ai-accelerated-dev/) | Agentic IDEs, AI pair programming, refactoring |
| 18 | [Ethics & Safety](18-ethics-safety/) | Governance, guardrails, bias, build vs buy |
| 19 | [System Design](19-system-design/) | Architecture design, model selection, trade-offs |
| 20 | [Freelance & Portfolio](20-freelance-portfolio/) | Portfolio building, client workflow, pricing |
| 21 | [Bootcamp Project](21-bootcamp-project/) | Enterprise AI solution, end-to-end development |

## Prerequisites

- Python 3.10+
- Basic command line familiarity
- An OpenAI account (for API key)
- A Pinecone account (free tier)

## Quick Start

```bash
# Clone this repository
git clone <repo-url>
cd ai-engineering

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter lab
```

See [setup.md](setup.md) for detailed environment setup including API keys.

## How to Use

1. **Follow modules in order** — each builds on the previous
2. **Read the README.md** in each module for theory and concepts
3. **Run the notebooks** for hands-on practice
4. **Complete the exercises** to solidify understanding
5. **Check resources.md** for supplementary materials

## Repository Structure

```
ai-engineering/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── setup.md               # Environment setup guide
├── 01-intro-ai-architecture/
│   ├── README.md          # Theory & concepts
│   ├── notebooks/         # Jupyter notebooks
│   ├── exercises/         # Practice tasks
│   └── resources.md       # External references
├── 02-python-for-ai/
│   └── ...
└── ...
```
