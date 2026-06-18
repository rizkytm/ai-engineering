# Module 16: System Scaling & Performance Optimization

## Overview

AI systems face unique scaling challenges: variable latency, high compute costs, and unpredictable load patterns. This module covers practical optimization techniques that directly impact user experience and operational costs.

## Learning Objectives

- Understand factors affecting AI system latency
- Implement caching strategies for responses and embeddings
- Design batch processing pipelines for throughput
- Build cost-aware routing systems
- Apply rate limiting and backoff for resilience
- Choose the right optimization technique for each scenario

---

## 1. Factors Affecting Latency in AI Systems

Latency in AI pipelines comes from multiple sources:

| Source | Typical Latency | Mitigation |
|--------|----------------|------------|
| Network round-trip | 50–200ms | Edge deployment, connection pooling |
| Token generation | 20–100ms/token | Streaming, smaller models |
| Embedding computation | 10–50ms | Caching, batching |
| Vector search | 5–50ms | Index tuning, sharding |
| Context assembly | 5–20ms | Query optimization |
| Post-processing | 1–10ms | Async pipelines |

**Key insight:** The biggest wins come from avoiding work entirely (caching) or doing less work (routing to smaller models).

---

## 2. Strategies for Reducing Response Time

### Avoid work with caching
Cache responses for repeated queries. A 100ms response becomes 5ms on cache hit.

### Do less work with model routing
Route simple queries to cheap/fast models, complex queries to powerful ones.

### Overlap work with streaming
Start sending tokens before the full response is generated. Users perceive 200ms TTFT (time-to-first-token) as "fast" even if total response time is 5 seconds.

### Parallelize independent steps
Run embedding, retrieval, and context assembly concurrently rather than sequentially.

### Reduce payload size
Stream instead of buffering. Return only what the user needs.

---

## 3. Streaming Responses for Better UX

Streaming transforms perceived performance by delivering the first token quickly and showing progress incrementally.

### Implementation Pattern

```python
async def stream_response(query: str):
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": query}],
        stream=True
    )
    async for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

### SSE (Server-Sent Events)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/chat")
async def chat(query: str):
    return StreamingResponse(
        stream_response(query),
        media_type="text/event-stream"
    )
```

### When to stream vs buffer

| Scenario | Use streaming |
|----------|--------------|
| Chat interfaces | Yes |
| Long-form generation | Yes |
| Short factual answers | Optional |
| API responses with structured output | No |
| Batch jobs | No |

---

## 4. Caching Strategies

### Response Caching

Cache complete LLM responses keyed by prompt hash.

```python
import hashlib
import redis.asyncio as redis

class ResponseCache:
    def __init__(self, redis_url: str, ttl: int = 3600):
        self.redis = redis.from_url(redis_url)
        self.ttl = ttl

    def _key(self, prompt: str, model: str) -> str:
        content = f"{model}:{prompt}"
        return f"llm:cache:{hashlib.sha256(content.encode()).hexdigest()}"

    async def get(self, prompt: str, model: str) -> str | None:
        return await self.redis.get(self._key(prompt, model))

    async def set(self, prompt: str, model: str, response: str):
        await self.redis.setex(self._key(prompt, model), self.ttl, response)
```

### Embedding Caching

Cache embeddings to avoid recomputing vectors for repeated text.

```python
class EmbeddingCache:
    def __init__(self, redis_url: str, ttl: int = 86400):
        self.redis = redis.from_url(redis_url)
        self.ttl = ttl

    async def get_or_compute(self, text: str, compute_fn) -> list[float]:
        key = f"emb:{hashlib.sha256(text.encode()).hexdigest()}"
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)
        embedding = await compute_fn(text)
        await self.redis.setex(key, self.ttl, json.dumps(embedding))
        return embedding
```

### Cache Invalidation

- **TTL-based:** Simple, automatic expiry. Good for stable data.
- **Version-based:** Prefix keys with a version number. Bump version on schema changes.
- **Event-driven:** Invalidate on write events. More complex but more precise.

---

## 5. Batch Processing vs Real-Time Processing

### Batch Processing

Process multiple inputs in a single API call or in parallel.

```python
import asyncio

async def batch_embed(texts: list[str], batch_size: int = 100) -> list[list[float]]:
    """Embed texts in batches."""
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )
        all_embeddings.extend([item.embedding for item in response.data])
    return all_embeddings
```

### Real-Time Processing

Process one request at a time with minimal latency. Use for user-facing endpoints.

### Decision Matrix

| Factor | Batch | Real-Time |
|--------|-------|-----------|
| Latency tolerance | High (minutes/hours) | Low (ms/seconds) |
| Throughput | High | Low-medium |
| Cost efficiency | Better (fewer API calls) | Higher per-request cost |
| Use cases | ETL, analytics, training | Chat, search, recommendations |

---

## 6. Cost Optimization

### Model Routing

Route queries to appropriate models based on complexity.

```python
class ModelRouter:
    def __init__(self):
        self.classifier = None  # lightweight classifier

    async def route(self, query: str) -> str:
        complexity = await self._classify_complexity(query)
        if complexity == "simple":
            return "gpt-3.5-turbo"  # $0.50/1M tokens
        elif complexity == "medium":
            return "gpt-4o-mini"    # $0.15/1M tokens input
        else:
            return "gpt-4o"         # $2.50/1M tokens input
```

### Token Counting and Cost Tracking

```python
import tiktoken

class CostTracker:
    def __init__(self):
        self.encoder = tiktoken.encoding_for_model("gpt-4")
        self.prices = {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        }

    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        prices = self.prices.get(model, {"input": 0, "output": 0})
        return (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000
```

### Combining Caching + Routing

```
Request → Cache Check → Cache Hit? → Return cached response
                    ↓ Miss
              Route to model → Generate → Cache response → Return
```

---

## 7. Connection Pooling and Request Batching

### Connection Pooling

Reuse HTTP connections to reduce handshake overhead.

```python
import httpx

# Long-lived client with connection pooling
client = httpx.AsyncClient(
    limits=httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20,
        keepalive_expiry=30
    )
)
```

### Request Batching

Accumulate requests over a short window and send as a batch.

```python
import asyncio
from collections import deque

class RequestBatcher:
    def __init__(self, batch_size: int = 10, max_wait_ms: int = 100):
        self.batch_size = batch_size
        self.max_wait = max_wait_ms / 1000
        self.queue: deque = deque()

    async def add(self, request):
        future = asyncio.get_event_loop().create_future()
        self.queue.append((request, future))

        if len(self.queue) >= self.batch_size:
            await self._flush()
        else:
            asyncio.get_event_loop().call_later(self.max_wait, lambda: asyncio.ensure_future(self._flush()))

        return await future
```

---

## 8. Rate Limiting and Backoff Strategies

### Rate Limiting

Protect your service from overload and manage API quota.

```python
import time
from collections import defaultdict

class TokenBucketRateLimiter:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate          # tokens per second
        self.capacity = capacity
        self.tokens = defaultdict(lambda: capacity)
        self.last_refill = defaultdict(time.time)

    async def acquire(self, key: str) -> bool:
        now = time.time()
        elapsed = now - self.last_refill[key]
        self.tokens[key] = min(
            self.capacity,
            self.tokens[key] + elapsed * self.rate
        )
        self.last_refill[key] = now

        if self.tokens[key] >= 1:
            self.tokens[key] -= 1
            return True
        return False
```

### Exponential Backoff

```python
import asyncio
import random

async def retry_with_backoff(func, max_retries: int = 5, base_delay: float = 1.0):
    for attempt in range(max_retries):
        try:
            return await func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
```

### Retry Decision Matrix

| Error | Retry? | Strategy |
|-------|--------|----------|
| 429 Rate Limit | Yes | Exponential backoff |
| 500 Server Error | Yes | Exponential backoff |
| 503 Service Unavailable | Yes | Exponential backoff |
| 400 Bad Request | No | Fix the request |
| 401 Unauthorized | No | Fix auth |
| Timeout | Maybe | Once with longer timeout |

---

## 9. When to Use Which Optimization Technique

### Decision Framework

| Problem | Solution | Complexity | Impact |
|---------|----------|------------|--------|
| Repeated queries | Response caching | Low | High |
| Slow embeddings | Embedding caching | Low | Medium |
| High throughput needs | Batch processing | Medium | High |
| Mixed query complexity | Model routing | Medium | High |
| Slow perceived response | Streaming | Low | High |
| API quota exhaustion | Rate limiting + caching | Low | High |
| Variable load | Connection pooling | Low | Medium |
| Cost reduction | Caching + routing | Medium | High |
| Large-scale ingestion | Batch + async | High | High |

### Optimization Priority

1. **Cache** — Lowest effort, highest impact for repeated queries
2. **Stream** — Immediate UX improvement
3. **Route** — Cost reduction for mixed workloads
4. **Batch** — Throughput for background jobs
5. **Pool** — Connection efficiency at scale
6. **Rate limit** — Resilience under load

### Combining Techniques

Most production systems combine multiple strategies:

```
User Request
  → Rate limit check
  → Cache lookup
  → If miss: model routing → LLM call → cache response
  → Stream tokens back to user
  → Track cost metrics
```

---

## Key Takeaways

1. **Avoid work first** — caching eliminates redundant computation
2. **Do less work** — route simple queries to cheap models
3. **Overlap work** — streaming improves perceived latency
4. **Track costs** — you can't optimize what you don't measure
5. **Layer strategies** — combine caching, routing, and streaming for maximum impact

---

## Next Steps

- **Notebook 01:** Implement response and embedding caching with Redis
- **Notebook 02:** Build batch processing pipelines with async
- **Notebook 03:** Create a cost-aware model routing system
- **Exercise:** Build a complete cost-optimized RAG pipeline
