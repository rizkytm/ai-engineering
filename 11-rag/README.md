# Module 11: Building Retrieval-Augmented Generation (RAG)

## Prerequisites

Set up your `.env` file in the project root with:

```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

Install dependencies:

```bash
pip install -r ../requirements.txt
```

## Learning Objectives

- Understand what RAG is and why it matters
- Build document ingestion and chunking pipelines
- Generate embeddings and store them in vector databases
- Implement retrieval pipelines with similarity search and ranking
- Optimize RAG with hybrid search, re-ranking, and prompt engineering
- Build a complete RAG chatbot using LangChain, Gemini, and Pinecone

---

## 1. What Is RAG?

Retrieval-Augmented Generation (RAG) combines a **Large Language Model (LLM)** with an **external knowledge retrieval system**. Instead of relying solely on the model's training data, RAG fetches relevant documents at query time and injects them into the LLM's context.

```
User Query → Retriever → Relevant Chunks → LLM + Context → Answer
```

The core idea: let the LLM generate answers grounded in real, up-to-date information rather than its static training data.

## 2. Why RAG?

| Problem | RAG Solution |
|---|---|
| **Hallucination** | Ground responses in retrieved source documents |
| **Stale knowledge** | Access real-time or regularly updated knowledge bases |
| **Domain specificity** | Inject proprietary or specialized content without fine-tuning |
| **Cost** | Cheaper than fine-tuning for knowledge-intensive tasks |
| **Transparency** | Cite sources; users can verify answers |

RAG gives you the reasoning power of LLMs without the cost or rigidity of fine-tuning for every knowledge update.

## 3. Core Components

### 3.1 Knowledge Base
The source of truth — documents, PDFs, web pages, databases, or any structured/unstructured data.

### 3.2 Embedding Model
Converts text into dense vector representations that capture semantic meaning. Examples: `text-embedding-3-small`, `bge-large`, `e5-large`.

### 3.3 Vector Store
Stores embeddings and enables fast similarity search. Examples: Pinecone, Chroma, Weaviate, Qdrant, FAISS.

### 3.4 Retriever
Queries the vector store to find the most relevant chunks for a given user query.

### 3.5 Generator (LLM)
Takes the retrieved chunks + user query and generates a coherent answer. Examples: Gemini, GPT-4, Claude.

## 4. Document Ingestion Pipeline

The ingestion pipeline converts raw documents into searchable chunks:

```
Raw Documents
    ↓
[ Load ] — Parse PDFs, HTML, text, databases
    ↓
[ Clean ] — Remove noise, normalize text
    ↓
[ Chunk ] — Split into manageable pieces
    ↓
[ Embed ] — Convert chunks to vectors
    ↓
[ Store ] — Index in vector database
```

Each step matters. Poor loading loses content. Bad chunking destroys context. Weak embeddings miss meaning.

## 5. Chunking Strategies

Chunking determines what the retriever can find. The strategy directly impacts retrieval quality.

### 5.1 Fixed-Size Chunking
Split text into chunks of N characters/tokens with overlap.

```python
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separator="\n"
)
chunks = splitter.split_text(document)
```

**Pros:** Simple, predictable, fast.
**Cons:** Splits mid-sentence, breaks semantic units.

### 5.2 Recursive Character Splitting
Tries separators in order (paragraphs → sentences → characters) to respect natural boundaries.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_text(document)
```

**Pros:** Better context preservation, respects document structure.
**Cons:** Slightly more complex.

### 5.3 Semantic Chunking
Groups sentences by semantic similarity — sentences about the same topic stay together.

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import ChatOpenAIEmbeddings

embeddings = ChatOpenAIEmbeddings(model="models/text-embedding-004")
splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile")
chunks = splitter.split_text(document)
```

**Pros:** Semantically coherent chunks, better retrieval precision.
**Cons:** Slower (requires embedding during splitting), more expensive.

### 5.4 Choosing a Strategy

| Strategy | Best For | Trade-off |
|---|---|---|
| Fixed-size | Quick prototypes, uniform documents | Loses context at boundaries |
| Recursive | Most production use cases | Slightly slower |
| Semantic | High-quality retrieval, diverse documents | Higher compute cost |

**Rule of thumb:** Start with recursive splitting. Move to semantic if retrieval quality needs improvement.

## 6. Embedding Documents

Embeddings convert text to vectors that capture meaning. Similar texts produce similar vectors.

### Choosing an Embedding Model

- **Dimensionality:** Higher dimensions = more expressiveness, higher storage cost
- **Domain:** General models vs. domain-specific (code, medical, legal)
- **Speed vs. quality:** Larger models are slower but more accurate

### Popular Models

| Model | Dimensions | Notes |
|---|---|---|
| `text-embedding-004` | 768 | Good general purpose |
| `text-embedding-3-small` | 1536 | OpenAI, balanced |
| `bge-large-en-v1.5` | 1024 | Strong open-source |
| `e5-large-v2` | 1024 | Microsoft, retrieval-optimized |

## 7. Vector Storage and Retrieval

### 7.1 Similarity Search
The default retrieval method. Computes cosine similarity (or dot product) between the query vector and stored vectors.

```
query_embedding → [cosine_similarity] → top-k results
```

### 7.2 Types of Distance Metrics

- **Cosine similarity:** Best for normalized vectors. Measures angle, not magnitude.
- **Dot product:** Fast. Assumes normalized embeddings.
- **Euclidean distance:** Measures raw distance in embedding space.

### 7.3 Filtering
Narrow results by metadata before or after similarity search:

```python
results = vector_store.similarity_search(
    query,
    k=5,
    filter={"source": "documentation", "year": 2024}
)
```

### 7.4 Ranking
Initial retrieval is approximate. Re-ranking refines the top results:

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

reranker = CohereRerank(model="rerank-v3.5", top_n=3)
compressor_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=retriever
)
```

## 8. RAG Optimization Techniques

### 8.1 Hybrid Search
Combine keyword-based (BM25) search with semantic search for best-of-both-worlds:

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_texts(chunks)
semantic_retriever = vector_store.as_retriever()

ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.3, 0.7]
)
```

**When to use:** Keywords matter (names, codes, specific terms) alongside semantic meaning.

### 8.2 Re-ranking
Pass initial retrieval results through a cross-encoder or learned reranker:

- **Cohere Rerank:** API-based, high quality
- **Cross-encoder:** Local, good performance
- **ColBERT:** Fast, late-interaction model

### 8.3 Query Transformation
Improve retrieval by transforming the user query:

- **Query rewriting:** Rewrite vague queries for clarity
- **HyDE:** Generate a hypothetical answer, embed it, search with that
- **Sub-questions:** Break complex queries into simpler ones

### 8.4 Prompt Engineering for RAG
The prompt template determines how the LLM uses retrieved context:

```python
template = """
Answer the question based on the following context.
If the context doesn't contain enough information, say "I don't have enough information to answer this."

Context:
{context}

Question: {question}

Answer:"""
```

**Best practices:**
- Instruct the model to use only provided context
- Include a fallback for insufficient information
- Ask for citations or source references
- Structure the context clearly

### 8.5 Evaluate RAG Quality

| Metric | What It Measures |
|---|---|
| **Faithfulness** | Is the answer grounded in the retrieved context? |
| **Answer relevance** | Does the answer address the question? |
| **Context precision** | Are the retrieved chunks relevant? |
| **Context recall** | Did retrieval capture all relevant information? |

Tools: RAGAS, DeepEval, Phoenix (Arize)

## 9. Common RAG Failure Modes

| Failure | Symptom | Fix |
|---|---|---|
| **Poor chunking** | Relevant info split across chunks | Adjust chunk size/overlap, use semantic chunking |
| **Weak embeddings** | Retrieval misses obvious matches | Switch embedding model, fine-tune embeddings |
| **No context found** | Model says "I don't know" | Expand retrieval (more chunks), try hybrid search |
| **Irrelevant retrieval** | Wrong chunks retrieved | Add metadata filtering, improve chunk quality |
| **Lost in the middle** | Model ignores context in the middle | Reorder context, use re-ranking |
| **Hallucination** | Model makes up facts despite context | Strengthen prompt instructions, use smaller context windows |

## 10. Building a RAG Chatbot with LangChain, OpenAI, and Pinecone

### Architecture

```
User Input
    ↓
[Query Transformation] — Rewrite for better retrieval
    ↓
[Retrieval] — Pinecone similarity search + metadata filter
    ↓
[Re-ranking] — Cross-encoder or Cohere rerank
    ↓
[Prompt Construction] — Inject context into template
    ↓
[Generation] — Gemini LLM produces answer
    ↓
[Response] — Answer with source citations
```

### Key Implementation

```python
from langchain_google_genai import ChatChatOpenAI, ChatOpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Initialize components
llm = ChatChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = ChatOpenAIEmbeddings(model="models/text-embedding-004")
vector_store = PineconeVectorStore(
    index_name="rag-knowledge-base",
    embedding=embeddings,
    namespace="docs"
)

# Create retrieval chain
prompt = PromptTemplate(
    template="""Use the following context to answer the question.
If you cannot answer from the context, say so.

Context:
{context}

Question: {question}

Answer:""",
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)

# Query
result = qa_chain.invoke({"query": "What is RAG?"})
print(result["result"])
for doc in result["source_documents"]:
    print(f"Source: {doc.metadata['source']}")
```

## Summary

RAG bridges the gap between LLM reasoning and real-world knowledge. The key decisions are:

1. **Chunking** — Start recursive, try semantic for quality
2. **Embeddings** — Match model to your domain and scale
3. **Retrieval** — Hybrid search outperforms single-method
4. **Ranking** — Re-ranking consistently improves precision
5. **Prompting** — Ground the LLM in retrieved context with clear instructions
6. **Evaluation** — Measure faithfulness, relevance, and recall

---

## Files in This Module

| File | Description |
|---|---|
| `notebooks/01-rag-fundamentals.ipynb` | End-to-end RAG pipeline walkthrough |
| `notebooks/02-chunking-strategies.ipynb` | Compare chunking approaches with visuals |
| `notebooks/03-rag-optimization.ipynb` | Hybrid search, re-ranking, evaluation |
| `exercises/exercise-01.md` | Hands-on practice problems |
| `resources.md` | Curated links and references |
