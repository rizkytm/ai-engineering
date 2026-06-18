# Module 07: Text Embeddings & Semantic Representation

> Peserta akan memahami text embeddings, cara kerjanya, dan bagaimana menggunakannya untuk semantic search, clustering, dan similarity-based applications.

## Learning Objectives

By the end of this module, you will be able to:

- Explain what text embeddings are and why they outperform Bag-of-Words
- Understand how embeddings capture semantic meaning in vector space
- Generate embeddings using OpenAI Embeddings API and open-source models
- Compute similarity between text using cosine similarity and other metrics
- Build a simple semantic search system
- Compare embedding quality across different models
- Visualize embeddings in 2D space

---

## 1. What Are Text Embeddings?

**Text embeddings** are dense vector representations of text — numeric arrays that capture the meaning of words, sentences, or documents. Similar texts produce similar vectors, enabling computers to "understand" semantic relationships.

```
"hello" → [0.02, -0.05, 0.13, ..., 0.08]   (768 dimensions)
"hi"    → [0.03, -0.04, 0.12, ..., 0.07]   (similar!)
"car"   → [0.21, 0.45, -0.33, ..., -0.12]  (very different)
```

**Key insight**: Embeddings encode *meaning*, not just characters or word counts.

---

## 2. Bag-of-Words vs Modern Embeddings

### Bag-of-Words (BoW)

Traditional approach: count word frequencies, ignore order.

| | "cat sat mat" | "mat sat cat" |
|---|---|---|
| cat | 1 | 1 |
| mat | 1 | 1 |
| sat | 1 | 1 |

**Problem**: Both sentences have identical BoW vectors despite potentially different meanings.

### Modern Embeddings

| Sentence | Embedding |
|----------|-----------|
| "The cat sat on the mat" | [0.02, -0.05, 0.13, ...] |
| "A feline rested on the rug" | [0.02, -0.04, 0.14, ...] |
| "The stock market crashed today" | [0.88, 0.45, -0.33, ...] |

**Why embeddings win**:
- Capture **semantic meaning** (feline ≈ cat)
- Handle **context** (word order matters)
- Support **similarity search** (not just keyword matching)
- Work with **new vocabulary** (generalize better)

---

## 3. How Embeddings Capture Semantic Meaning

### The Distributional Hypothesis

> "You shall know a word by the company it keeps." — J.R. Firth (1957)

Models learn that words appearing in similar contexts have similar meanings:

- "I drank **coffee** every morning" vs "I drank **tea** every morning"
- "coffee" and "tea" appear in similar contexts → similar embeddings

### Training Process

1. **Pre-training**: Model reads billions of text examples
2. **Learning patterns**: Words close together get similar vectors
3. **Dimensionality**: Meaning compressed into 256-3072 dimensions
4. **Semantic clustering**: Related concepts cluster together in vector space

```
Vector Space (2D visualization):

    'king' ●
              ● 'queen'
    'man' ●
              ● 'woman'
    'prince' ●
              ● 'princess'

                    ● 'car'
                    ● 'truck'
```

---

## 4. Embedding Dimensions and Vector Space

### Dimensions

Each embedding is a vector with a fixed number of dimensions:

| Model | Dimensions | Description |
|-------|-----------|-------------|
| `text-embedding-004` (Gemini) | 768 | Google's latest embedding model |
| `text-embedding-005` (Gemini) | 768 | Latest Gemini embedding model |
| `all-MiniLM-L6-v2` | 384 | Lightweight sentence-transformer |
| `text-embedding-3-large` (OpenAI) | 3072 | OpenAI's largest model |

**Higher dimensions** → more nuanced representations, but slower and more memory-intensive.

### Vector Space Properties

- **High-dimensional**: Usually 256-4096 dimensions
- **Dense**: Most values are non-zero (unlike sparse BoW vectors)
- **Normalized**: Typically unit vectors (magnitude = 1) for cosine similarity
- **Semantic**: Meaningful directions in space correspond to concepts

---

## 5. Semantic Similarity and Cosine Similarity

### Cosine Similarity

Measures the angle between two vectors:

```
cosine_similarity(A, B) = (A · B) / (|A| × |B|)
```

| Score | Meaning |
|-------|---------|
| 1.0 | Identical meaning |
| 0.8-0.9 | Very similar |
| 0.5-0.7 | Somewhat similar |
| 0.0-0.3 | Different/unrelated |
| -0.1-0.0 | Opposite (rare) |

### Example Calculations

```python
import numpy as np

# "cat" embedding (simplified to 3D for illustration)
cat = np.array([0.9, 0.1, 0.3])
kitten = np.array([0.8, 0.2, 0.4])
car = np.array([0.1, 0.8, 0.2])

# Cosine similarity
cos_sim = np.dot(cat, kitten) / (np.linalg.norm(cat) * np.linalg.norm(kitten))
# ≈ 0.95 (very similar)

cos_sim_car = np.dot(cat, car) / (np.linalg.norm(cat) * np.linalg.norm(car))
# ≈ 0.25 (different)
```

### Other Similarity Metrics

| Metric | Formula | Best For |
|--------|---------|----------|
| **Cosine similarity** | angle between vectors | Text similarity (recommended) |
| **Dot product** | sum(a_i × b_i) | When magnitude matters |
| **Euclidean distance** | sqrt(sum(a_i - b_i)²) | Geometric proximity |

---

## 6. Using OpenAI Embeddings API

### Setup

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
```

### Generating Embeddings

```python
# Single text
result = genai.embed_content(
    model="models/text-embedding-004",
    content="What is machine learning?"
)
embedding = result["embedding"]  # List of 768 floats

# Multiple texts (batch)
texts = [
    "What is machine learning?",
    "How does deep learning work?",
    "What's the weather today?"
]
results = genai.embed_content(
    model="models/text-embedding-004",
    content=texts
)
embeddings = results["embedding"]  # List of 3 lists
```

### Key Features

- **Task type**: Optional parameter for search, clustering, classification
- **Batch support**: Embed multiple texts efficiently
- **Output dimensionality**: Can reduce dimensions (e.g., 256 instead of 768)
- **Rate limits**: Free tier has generous limits for development

---

## 7. Comparing Embedding Models

### API-Based (Cloud)

| Provider | Model | Dimensions | Pros | Cons |
|----------|-------|-----------|------|------|
| Google | text-embedding-004 | 768 | Fast, accurate, free tier | Requires internet |
| OpenAI | text-embedding-3-large | 3072 | Very accurate | Paid, larger dimensions |
| Cohere | embed-english-v3.0 | 1024 | Multilingual | Paid |

### Open-Source (Local)

| Model | Dimensions | Pros | Cons |
|-------|-----------|------|------|
| all-MiniLM-L6-v2 | 384 | Fast, lightweight | Lower accuracy |
| all-mpnet-base-v2 | 768 | Good balance | Slower |
| BGE-large-en | 1024 | High accuracy | Larger model |

### When to Choose What

- **API-based**: Quick prototyping, best accuracy, don't need local deployment
- **Open-source**: Privacy requirements, offline use, cost control at scale
- **Hybrid**: Use API for development, migrate to open-source for production

---

## 8. Use Cases

### 1. Semantic Search
Find relevant documents based on meaning, not just keywords.
```
Query: "how to fix slow database"
→ Finds: "optimizing SQL query performance", "database indexing guide"
```

### 2. Recommendation Systems
Suggest similar content based on embedding similarity.
```
User liked: "Introduction to Neural Networks"
→ Recommend: "Deep Learning Fundamentals", "Perceptron Explained"
```

### 3. Clustering
Group similar documents without labels.
```
Cluster 1: ["Python tutorial", "Learn Python", "Python basics"]
Cluster 2: ["JavaScript guide", "JS fundamentals", "Web dev intro"]
```

### 4. Classification
Use embeddings as features for classification models.
```
Input: "Great product, love it!" → Embedding → Positive review
Input: "Terrible quality, waste of money" → Embedding → Negative review
```

### 5. Anomaly Detection
Identify outliers that don't fit typical patterns.
```
Normal: embeddings cluster around [0.1, 0.3, 0.2, ...]
Anomaly: embedding at [0.9, -0.7, 0.8, ...] → suspicious
```

---

## 9. Best Practices

1. **Normalize vectors** before computing similarity
2. **Choose the right model** for your use case (accuracy vs speed vs cost)
3. **Batch API calls** to reduce latency and cost
4. **Cache embeddings** for frequently accessed texts
5. **Test with real data** — embedding quality varies by domain

---

## Module Contents

- [Notebook 01: Embeddings Basics](notebooks/01-embeddings-basics.ipynb) — Generate and visualize embeddings with OpenAI API
- [Notebook 02: Similarity Search](notebooks/02-similarity-search.ipynb) — Build a similarity search system
- [Notebook 03: Embedding Comparison](notebooks/03-embedding-comparison.ipynb) — Compare different embedding models
- [Exercise 01](exercises/exercise-01.md) — Practice exercises
- [Resources](resources.md) — Links and references
