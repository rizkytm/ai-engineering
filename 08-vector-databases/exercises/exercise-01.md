# Exercise 01: Vector Databases & Semantic Search

## Prerequisites

- Pinecone API key (free tier: [pinecone.io](https://www.pinecone.io/))
- OpenAI API key (for embeddings)
- Python packages: `pip install pinecone python-dotenv openai faiss-cpu numpy`

Create a `.env` file:

```
PINECONE_API_KEY=your-pinecone-key
OPENAI_API_KEY=your-openai-key
```

---

## Part 1: Pinecone Setup and CRUD Operations

### Objective

Create a Pinecone index, upsert vectors, query them, and clean up.

### Instructions

1. Create a Pinecone index named `exercise-vectors` with dimension 1536 and cosine metric
2. Upsert at least 5 vectors with text metadata:
   ```python
   vectors = [
       {
           "id": "v1",
           "values": [...],  # 1536-dimension embedding
           "metadata": {"text": "...", "category": "...", "source": "..."}
       },
       # ... more vectors
   ]
   ```
3. Query the index with a vector and print the top 3 results with scores
4. Delete the index when done

### Expected Output

```
Created index: exercise-vectors
Upserted 5 vectors.
Query results:
  1. v3 (score: 0.9234): "Text of vector v3"
  2. v1 (score: 0.8756): "Text of vector v1"
  3. v5 (score: 0.8102): "Text of vector v5"
Deleted index: exercise-vectors.
```

### Solution Skeleton

```python
from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Create index
# ...

# Step 2: Generate embeddings and upsert
# texts = ["...", "...", ...]
# response = client.embeddings.create(model="text-embedding-3-small", input=texts)
# embeddings = [item.embedding for item in response.data]
# ...

# Step 3: Query
# ...

# Step 4: Cleanup
# ...
```

---

## Part 2: Semantic Search Engine

### Objective

Build a semantic search engine over a collection of technical documents.

### Instructions

1. Create a collection of 10+ documents with metadata (topic, difficulty, language)
2. Generate embeddings using `text-embedding-3-small`
3. Store them in a new Pinecone index
4. Implement a `search(query_text, top_k, filter_dict)` function that:
   - Embeds the query text
   - Searches Pinecone
   - Returns structured results with text and metadata
5. Test with these queries:
   - "How do I learn to code?"
   - "What tools are used for deploying applications?"
   - "Explain how neural networks work"
6. For each query, note which results are relevant

### Expected Output

```
Query: "How do I learn to code?"
  1. (0.89) "Python is great for beginners..."
  2. (0.82) "Start with HTML/CSS fundamentals..."
  3. (0.75) "Online platforms like Codecademy..."

Relevant results: 1, 2 (2/3 = 66.6% precision)
```

---

## Part 3: Similarity Score Comparison

### Objective

Understand how different similarity metrics affect results.

### Instructions

1. Create two indexes for the same data:
   - Index A: `cosine` metric
   - Index B: `dotproduct` metric
2. Upsert the same vectors into both (normalize vectors for dotproduct)
3. Run the same 5 queries on both indexes
4. Record the scores and top results for each
5. Write a comparison:
   - Do the rankings change?
   - Are the score magnitudes different?
   - Which metric gives more intuitive results?

### Questions to Answer

1. When would you prefer cosine similarity over dot product?
2. What happens to dot product scores when vectors have different magnitudes?
3. Which metric is most appropriate for text embeddings? Why?

---

## Part 4: Metadata Filtering

### Objective

Practice combining semantic search with metadata filters.

### Instructions

1. Use the document collection from Part 2
2. Run these filtered searches and document results:

   | Query | Filter | Expected Results |
   |-------|--------|------------------|
   | "programming concepts" | `topic == "programming"` | Only programming docs |
   | "advanced topics" | `difficulty == "advanced"` | Only advanced docs |
   | "data handling" | `topic in ["databases", "data-science"]` | DB and data science docs |
   | "beginner Python" | `topic == "programming" AND language == "Python"` | Beginner Python docs |

3. For each, note:
   - How many results were returned?
   - Did the filter correctly narrow results?
   - Did semantic ranking still make sense within the filtered set?

---

## Bonus: Benchmark FAISS vs Pinecone

### Objective

Compare local FAISS performance against Pinecone for different dataset sizes.

### Instructions

1. Generate random vectors at these scales:
   - 1,000 vectors (dimension=1536)
   - 10,000 vectors
   - 100,000 vectors
2. For each scale, measure:
   - **Index build time**: FAISS (HNSW) vs Pinecone upsert
   - **Query time**: 100 queries, average latency
   - **Memory/disk usage**
3. Create a results table:

   | Vectors | FAISS Build | Pinecone Build | FAISS Query (avg) | Pinecone Query (avg) |
   |---------|-------------|----------------|--------------------|-----------------------|
   | 1,000   | ...         | ...            | ...                | ...                   |
   | 10,000  | ...         | ...            | ...                | ...                   |
   | 100,000 | ...         | ...            | ...                | ...                   |

4. Write a 3-paragraph summary:
   - At what scale does each solution shine?
   - What are the cost implications?
   - What would you choose for a production app with 500K documents?

### Hints

- Use `time.time()` for timing
- FAISS memory: use `index.sa_code_size()` or estimate from vector count × dimension × 4 bytes
- Pinecone build time includes network latency — isolate it by subtracting a baseline RTT
