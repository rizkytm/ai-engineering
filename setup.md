# Environment Setup Guide

## 1. Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Jupyter Notebook

```bash
# Register the venv as a Jupyter kernel
python -m ipykernel install --user --name=ai-engineering

# Start Jupyter Lab
jupyter lab
```

Select the `ai-engineering` kernel when running notebooks.

## 3. API Keys

Create a `.env` file in the project root:

```env
# OpenAI API (https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone (https://app.pinecone.io/)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=your_index_name

# LangSmith (https://smith.langchain.com/) — optional, for observability modules
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ai-engineering
```

**Never commit `.env` to version control.**

## 4. Verify Installation

```bash
python -c "
import numpy as np
import pandas as pd
import torch
from langchain_openai import ChatOpenAI
print('All imports successful')
print(f'NumPy: {np.__version__}')
print(f'Pandas: {pd.__version__}')
print(f'PyTorch: {torch.__version__}')
import openai
print(f'OpenAI: {openai.__version__}')
"
```

## 5. Tool Accounts

| Tool | Purpose | Sign Up |
|------|---------|---------|
| OpenAI | GPT API access | [platform.openai.com](https://platform.openai.com/api-keys) |
| Pinecone | Vector database | [app.pinecone.io](https://app.pinecone.io/) |
| LangSmith | Observability (optional) | [smith.langchain.com](https://smith.langchain.com/) |
| Hugging Face | Model hub | [huggingface.co](https://huggingface.co/) |
