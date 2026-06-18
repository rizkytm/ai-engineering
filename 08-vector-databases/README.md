# Module 08: Vector Databases & Semantic Search

## Learning Objectives

By the end of this module, you will be able to:

- Explain the difference between keyword search and semantic search
- Understand how vector search works under the hood (ANN, HNSW, IVF)
- Read and interpret similarity scores from vector queries
- Create, populate, and query a Pinecone index
- Use metadata filtering to narrow search results
- Build a semantic search engine from scratch
- Set up FAISS for local vector storage and prototyping
- Choose between managed (Pinecone) and self-hosted (FAISS, Chroma) solutions

---

## 1. Keyword Search vs Semantic Search

### Keyword Search (Traditional)

Traditional search relies on exact token matching. Search engines like Elasticsearch use **BM25** or **TF-IDF** to rank results based on term frequency and inverse document frequency.

**Limitations:**
- Misses synonyms ("car" won't match "automobile")
- Ignores context ("bank" means the same as "bank" regardless of context)
- Requires exact term overlap to find matches
- Struggles with natural language queries

### Semantic Search (Vector-Based)

Semantic search understands **meaning**. It converts text into high-dimensional vectors (embeddings) where similar concepts are close together in vector space.

**Advantages:**
- Finds conceptually similar content, even with different wording
- Understands context and nuance
- Works with natural language queries
- Handles synonyms and paraphrases naturally

**Example:**

| Query | Keyword Match | Semantic Match |
|-------|--------------|----------------|
| "how to fix a broken heart" | Documents with "broken heart" | Emotional recovery articles, self-help content |
| "affordable electric vehicles for families" | Documents with "affordable" + "electric" + "vehicles" | Budget EVs, family cars, commuter vehicles |

---

## 2. How Vector Search Works

### Embeddings

Text is converted to dense vectors using embedding models. These vectors capture semantic meaning:

```
"Machine learning is a subset of AI" → [0.23, -0.15, 0.87, ..., 0.42]  (768-1536 dimensions)
```

### Approximate Nearest Neighbor (ANN)

Exact nearest neighbor search is O(n) — too slow for millions of vectors. ANN algorithms trade perfect accuracy for massive speed gains.

**Key ANN Algorithms:**

#### HNSW (Hierarchical Navigable Small World)
- Builds a multi-layer graph where each node connects to nearby neighbors
- Top layer: sparse, long-range connections (fast traversal)
- Bottom layer: dense, local connections (precise search)
- **Pros:** Excellent query performance, high recall
- **Cons:** High memory usage (~3-10x the vector data), slow to build
- **Used by:** Pinecone, Weaviate, Qdrant

#### IVF (Inverted File Index)
- Partitions vectors into clusters (Voronoi cells)
- At query time, searches only the nearest clusters (not all vectors)
- **Pros:** Lower memory than HNSW, faster index building
- **Cons:** Lower recall at very high speeds
- **Often combined with:** Product Quantization (IVF-PQ) for compression

#### Product Quantization (PQ)
- Compresses vectors by splitting them into sub-vectors and quantizing each
- Reduces memory by 4-32x with minimal accuracy loss
- **Used as:** Compression layer under HNSW or IVF

### How Search Works at Query Time

```
1. Convert query text → embedding vector
2. Find nearest vectors in the index using the ANN algorithm
3. Return top-k results with similarity scores
```

---

## 3. Similarity Scoring and Reading Results

### Cosine Similarity (most common)

Measures the angle between two vectors, ignoring magnitude:

```
cosine_sim(A, B) = (A · B) / (||A|| × ||B||)
```

**Range:** -1 to +1
- **1.0** = identical direction (perfect match)
- **0.0** = orthogonal (unrelated)
- **-1.0** = opposite (opposite meaning)

### Dot Product

```
dot(A, B) = Σ(aᵢ × bᵢ)
```

Use when vectors are normalized. Range depends on vector magnitude.

### Euclidean Distance (L2)

```
dist(A, B) = √Σ(aᵢ - bᵢ)²
```

Smaller = more similar. Used less frequently for text embeddings.

### Reading Pinecone Results

```python
results = index.query(vector=query_embedding, top_k=5)

for match in results['matches']:
    print(f"ID:      {match['id']}")
    print(f"Score:   {match['score']}")    # Cosine similarity (0 to 1)
    print(f"Metadata: {match['metadata']}")
```

**Score Interpretation (cosine similarity):**
- **0.9 - 1.0:** Very strong match
- **0.7 - 0.9:** Strong match
- **0.5 - 0.7:** Moderate match
- **< 0.5:** Weak match (may still be relevant depending on domain)

---

## 4. Pinecone: Managed Vector Database

### Getting a Free Pinecone API Key

1. Go to [https://www.pinecone.io/](https://www.pinecone.io/)
2. Click **Sign Up** (free tier available)
3. Create an account with email or Google/GitHub
4. Once logged in, navigate to **API Keys** in the dashboard
5. Click **Create API Key**
6. Copy the API key and save it

### Storing Your API Key

Create a `.env` file in your project root:

```
PINECONE_API_KEY=your-api-key-here
```

Never commit `.env` files to version control. Load them using:

```python
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
```

### Core Operations

```python
from pinecone import Pinecone, ServerlessSpec

# Initialize
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index
pc.create_index(
    name="my-index",
    dimension=1536,          # Must match embedding model output
    metric="cosine",         # cosine, dotproduct, or euclidean
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Connect to index
index = pc.Index("my-index")

# Upsert vectors
index.upsert(vectors=[
    {
        "id": "vec1",
        "values": [0.1, 0.2, ...],  # Embedding vector
        "metadata": {"text": "Machine learning basics", "category": "ML"}
    }
])

# Query
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=5,
    include_metadata=True,
    filter={"category": {"$eq": "ML"}}  # Metadata filtering
)
```

### Metadata Filtering

Filter results by metadata fields before or during the search:

```python
# Equality filter
filter={"category": {"$eq": "ML"}}

# Inequality filter
filter={"price": {"$gte": 10, "$lte": 50}}

# Logical operators
filter={
    "$and": [
        {"category": {"$eq": "ML"}},
        {"difficulty": {"$in": ["beginner", "intermediate"]}}
    ]
}

# Text contains
filter={"tags": {"$in": ["python", "deep-learning"]}}
```

---

## 5. FAISS for Local Prototyping

### What is FAISS?

**Facebook AI Similarity Search** is a library (not a service) for efficient similarity search and clustering of dense vectors. It runs entirely on your local machine.

### Advantages
- No API keys or cloud accounts needed
- No data leaves your machine (privacy)
- Extremely fast (optimized C++ with GPU support)
- Free and open source

### Disadvantages
- No built-in persistence (must save/load manually)
- No metadata filtering (you filter after retrieval)
- No managed infrastructure
- Manual index management

### Basic Usage

```python
import faiss
import numpy as np

# Create index
dimension = 1536
index = faiss.IndexFlatL2(dimension)  # Exact search

# Add vectors (must be numpy float32)
vectors = np.random.random((1000, dimension)).astype('float32')
index.add(vectors)

# Search
query = np.random.random((1, dimension)).astype('float32')
distances, indices = index.search(query, k=5)
```

### HNSW in FAISS

```python
# HNSW index (approximate, faster for large datasets)
index = faiss.IndexHNSWFlat(dimension, 32)  # 32 = graph connectivity
index.hnsw.efSearch = 64  # Search accuracy (higher = better, slower)
```

---

## 6. Vector Database Architecture Considerations

### Key Design Decisions

| Decision | Options | Trade-offs |
|----------|---------|------------|
| **Storage** | In-memory vs disk-based | Speed vs capacity |
| **Indexing** | HNSW vs IVF-PQ | Memory vs speed vs accuracy |
| **Consistency** | Strong vs eventual | Latency vs durability |
| **Sharding** | By collection, by range, random | Query complexity vs throughput |
| **Replication** | Leader-follower vs multi-leader | Consistency vs availability |

### Production Architecture

```
Application Layer
    ↓
Query Router (load balancing, caching)
    ↓
Vector Database Cluster
    ├── Primary Index (write)
    ├── Replica Indexes (read)
    └── Metadata Store (SQL/NoSQL)
    ↓
Embedding Service (model serving)
    ↓
Object Storage (raw documents)
```

### Performance Optimization

- **Pre-filtering:** Use metadata filters to reduce the search space before ANN lookup
- **Embedding caching:** Cache frequently used embeddings to reduce API calls
- **Batch operations:** Upsert vectors in batches (100-1000 at a time)
- **Index tuning:** Adjust HNSW `efSearch` and `M` parameters for your accuracy/speed requirements

---

## 7. When to Use Managed vs Self-Hosted

### Managed (Pinecone, Weaviate Cloud, Qdrant Cloud)

**Best for:**
- Rapid prototyping and MVPs
- Teams without infrastructure expertise
- When you need high availability and scaling
- When you don't want to manage servers

**Trade-offs:**
- Cost at scale (per-vector pricing)
- Vendor lock-in
- Data leaves your infrastructure

### Self-Hosted (FAISS, Chroma, Milvus, Qdrant)

**Best for:**
- Cost-sensitive workloads at scale
- Data privacy/regulatory requirements
- Custom optimization needs
- Learning and experimentation

**Trade-offs:**
- Infrastructure management overhead
- Need DevOps expertise
- Must handle scaling yourself

### Quick Decision Guide

| Scenario | Recommendation |
|----------|---------------|
| Learning/prototyping | FAISS (free, local) |
| MVP with <1M vectors | Pinecone free tier |
| Production, <10M vectors | Pinecone or managed Weaviate |
| Production, >10M vectors, cost-sensitive | Self-hosted Milvus or Qdrant |
| On-premise, strict data privacy | FAISS or self-hosted Qdrant |
| Real-time search with filtering | Pinecone or Qdrant |

---

## Module Structure

```
08-vector-databases/
├── README.md                    ← You are here
├── resources.md                 ← Links and references
├── notebooks/
│   ├── 01-pinecone-basics.ipynb
│   ├── 02-semantic-search.ipynb
│   └── 03-faiss-local.ipynb
└── exercises/
    └── exercise-01.md
```

## Setup Requirements

```bash
pip install pinecone python-dotenv sentence-transformers openai faiss-cpu numpy
```

Create a `.env` file in this directory:

```
PINECONE_API_KEY=your-pinecone-api-key
```

---

## Next Steps

Proceed to the notebooks in order, starting with [01-pinecone-basics.ipynb](notebooks/01-pinecone-basics.ipynb).
