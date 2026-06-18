# Module 01: Introduction to AI Architecture & System Engineering

> Peserta akan memahami landscape AI modern, perbedaan AI/ML/DL/GenAI, peran AI Engineer, serta cara membaca arsitektur produk AI dari sisi sistem.

## Learning Objectives

By the end of this module, you will be able to:

- Distinguish between AI, Machine Learning, Deep Learning, and Generative AI
- Trace the evolution of AI from rule-based systems to generative AI
- Analyze AI usage across industries (SaaS, fintech, healthcare, e-commerce)
- Differentiate roles: Data Scientist, ML Engineer, AI System Engineer
- Identify core components of an AI system: data source, model layer, inference layer, application layer
- Draw architecture diagrams for AI products
- Set up your development environment and make your first API call

---

## 1. What is AI? A Taxonomy

```
Artificial Intelligence (AI)
├── Machine Learning (ML)
│   ├── Traditional ML (Random Forest, SVM, XGBoost)
│   └── Deep Learning (DL)
│       ├── CNN (Computer Vision)
│       ├── RNN/LSTM (Sequential Data)
│       └── Transformer (NLP, Multimodal)
│           └── Large Language Models (LLM)
│               └── Generative AI (GenAI)
```

### AI (Artificial Intelligence)
The broadest concept — machines performing tasks that typically require human intelligence. Includes rule-based systems, expert systems, and machine learning.

### Machine Learning (ML)
A subset of AI where systems learn patterns from data rather than being explicitly programmed. Key paradigms:
- **Supervised learning**: Learn from labeled data (classification, regression)
- **Unsupervised learning**: Find structure in unlabeled data (clustering, dimensionality reduction)
- **Reinforcement learning**: Learn through trial and error with rewards

### Deep Learning (DL)
ML using neural networks with multiple layers. Excels at unstructured data (text, images, audio). Requires large datasets and compute.

### Generative AI (GenAI)
AI that creates new content — text, images, code, audio. Built on foundation models (large pre-trained models) like GPT, Gemini, Llama, Claude.

---

## 2. Evolution of AI

| Era | Period | Approach | Example |
|-----|--------|----------|---------|
| Rule-Based | 1950s-1980s | Hand-coded if-then rules | Expert systems, ELIZA |
| Statistical ML | 1990s-2010s | Learn from structured data | Spam filters, recommendation |
| Deep Learning | 2012-2020 | Neural networks, big data | ImageNet, AlphaGo |
| Foundation Models | 2020-Present | Pre-trained + fine-tuned | GPT-4, Gemini, Claude |
| Agentic AI | 2024-Present | Autonomous agents + tools | AutoGPT, Devin, Cursor |

**Key insight**: Each era didn't replace the previous — they added new capabilities. Rule-based systems still exist in production.

---

## 3. AI in Industry

### SaaS
- **Use cases**: Smart search, content generation, automated customer support, code completion
- **Example**: Notion AI, GitHub Copilot, Intercom Fin

### Fintech
- **Use cases**: Fraud detection, credit scoring, algorithmic trading, document processing
- **Example**: Stripe Radar, Ant Group credit scoring

### Healthcare
- **Use cases**: Medical image analysis, drug discovery, clinical documentation, diagnostics
- **Example**: Google Med-PaLM, PathAI

### E-commerce
- **Use cases**: Product recommendations, dynamic pricing, visual search, inventory forecasting
- **Example**: Amazon recommendation engine, Shopify Magic

---

## 4. AI Roles: Who Does What?

| Role | Focus | Skills |
|------|-------|--------|
| **Data Scientist** | Analyze data, build models, extract insights | Statistics, SQL, Python, ML, visualization |
| **ML Engineer** | Productionize models, build training pipelines | ML frameworks, MLOps, system design |
| **AI System Engineer** | Build AI-powered products and services | APIs, backend, orchestration, deployment |

**This curriculum focuses on the AI System Engineer role** — building end-to-end AI products, not just training models.

```
Data Scientist → "What patterns exist in this data?"
ML Engineer → "How do we train and deploy this model at scale?"
AI System Engineer → "How do we build a product that uses AI effectively?"
```

---

## 5. Anatomy of an AI System

Every AI product has these layers:

```
┌─────────────────────────────────────────┐
│           APPLICATION LAYER             │
│   (Chat UI, API endpoint, Dashboard)    │
├─────────────────────────────────────────┤
│          ORCHESTRATION LAYER            │
│   (LangChain, prompt management,        │
│    tool routing, memory)                │
├─────────────────────────────────────────┤
│           INFERENCE LAYER               │
│   (LLM API calls, model serving,        │
│    embedding generation)                │
├─────────────────────────────────────────┤
│            MODEL LAYER                  │
│   (GPT-4, Gemini, Llama,               │
│    fine-tuned models)                   │
├─────────────────────────────────────────┤
│            DATA LAYER                   │
│   (Vector DB, SQL DB, file storage,     │
│    knowledge base)                      │
├─────────────────────────────────────────┤
│          DATA SOURCE LAYER              │
│   (User input, documents, APIs,         │
│    databases, web scraping)             │
└─────────────────────────────────────────┘
```

### Example: AI Chatbot with RAG

| Layer | Component |
|-------|-----------|
| Data Source | PDF documents, web pages |
| Data | Pinecone vector database |
| Model | Gemini embedding + Gemini Pro |
| Inference | Google AI API |
| Orchestration | LangChain (retrieval + prompt assembly) |
| Application | FastAPI endpoint + React frontend |

---

## 6. AI Engineer Toolkit

| Tool | Purpose |
|------|---------|
| **Python** | Primary language for AI engineering |
| **OpenAI API** | LLM inference (text generation, embeddings) |
| **LangChain** | Orchestration framework for LLM workflows |
| **Pinecone** | Vector database for semantic search |
| **Hugging Face** | Model hub, pre-trained models, datasets |
| **FastAPI** | Backend API framework |
| **Docker** | Containerization for deployment |
| **Git** | Version control |

---

## 7. Your First AI API Call

In the next notebook, you'll:
1. Install and configure the Gemini Python SDK
2. Set up API key management with `.env`
3. Send your first prompt to Gemini
4. Understand the request-response format

→ See [notebooks/01-first-api-call.ipynb](notebooks/01-first-api-call.ipynb)

---

## 8. Architecture Diagram Practice

In the hands-on notebook, you'll practice:
- Drawing AI system architectures using ASCII/Mermaid diagrams
- Mapping components to the layers framework
- Analyzing existing AI products

→ See [notebooks/02-architecture-diagram.ipynb](notebooks/02-architecture-diagram.ipynb)

---

## Exercises

- [Exercise 01: AI Landscape & Architecture](exercises/exercise-01.md)

## Resources

- [Resources & References](resources.md)
