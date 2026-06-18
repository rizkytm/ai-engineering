# Exercise 01: System Scaling & Performance Optimization

## Overview

Build practical optimization systems for AI pipelines. Complete all parts to earn full credit.

---

## Part 1: Response Caching

### Objective

Implement a response cache for an LLM-powered endpoint that handles repeated queries efficiently.

### Requirements

1. Create a `ResponseCache` class that:
   - Stores LLM responses keyed by prompt hash
   - Supports TTL-based expiration
   - Tracks cache hits and misses
   - Calculates hit rate

2. Integrate the cache with a mock LLM endpoint:
   - Check cache before calling LLM
   - Store responses after generation
   - Return cached responses instantly

### Starter Code

```python
import hashlib
import json
import time
from typing import Optional

class ResponseCache:
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self._store = {}
        self.hits = 0
        self.misses = 0

    def _key(self, prompt: str, model: str) -> str:
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get(self, prompt: str, model: str) -> Optional[str]:
        # TODO: Implement cache lookup with TTL check
        pass

    def set(self, prompt: str, model: str, response: str):
        # TODO: Implement cache storage
        pass

    @property
    def hit_rate(self) -> float:
        # TODO: Calculate hit rate
        pass
```

### Tests

```python
async def test_response_cache():
    cache = ResponseCache(ttl=5)

    # Simulate LLM calls
    async def mock_llm(prompt: str) -> str:
        await asyncio.sleep(0.1)
        return f"Response to: {prompt}"

    # First call should miss
    result1 = await mock_llm("What is Python?")
    cache.set("What is Python?", "gpt-4", result1)
    assert cache.get("What is Python?", "gpt-4") == result1
    assert cache.misses == 0  # just set, no get yet

    # Second call should hit
    cached = cache.get("What is Python?", "gpt-4")
    assert cached is not None
    assert cache.hits == 1

    # Different prompt should miss
    cached = cache.get("What is Java?", "gpt-4")
    assert cached is None
    assert cache.misses == 1

    print(f"Hit rate: {cache.hit_rate:.1%}")
    print("All tests passed!")
```

---

## Part 2: Batch Processing Pipeline

### Objective

Build a batch processing pipeline that processes multiple documents concurrently with rate limiting.

### Requirements

1. Create a `BatchProcessor` class that:
   - Accepts a list of documents
   - Processes them concurrently with configurable concurrency limit
   - Handles errors gracefully (retry on failure)
   - Returns results in order

2. Implement rate limiting:
   - Respect a maximum requests per second limit
   - Use token bucket or sliding window algorithm

### Starter Code

```python
import asyncio
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class BatchResult:
    successes: list[Any]
    failures: list[dict]
    total_time_ms: float
    items_per_second: float

class BatchProcessor:
    def __init__(self, max_concurrent: int = 10, rate_limit: float = 50.0):
        self.max_concurrent = max_concurrent
        self.rate_limit = rate_limit  # requests per second
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._tokens = rate_limit
        self._last_refill = time.time()

    async def _acquire_token(self):
        # TODO: Implement token bucket rate limiting
        pass

    async def process_item(self, item: Any, process_fn: Callable) -> Any:
        # TODO: Implement with semaphore and rate limiting
        pass

    async def process_batch(
        self,
        items: list[Any],
        process_fn: Callable,
        max_retries: int = 3
    ) -> BatchResult:
        # TODO: Implement batch processing with error handling
        pass
```

### Tests

```python
async def test_batch_processor():
    processor = BatchProcessor(max_concurrent=5, rate_limit=20.0)

    async def slow_process(item: str) -> str:
        await asyncio.sleep(0.05)
        if item == "fail":
            raise ValueError("Processing failed")
        return f"processed_{item}"

    items = [f"item_{i}" for i in range(20)] + ["fail"]
    result = await processor.process_batch(items, slow_process)

    assert len(result.successes) == 20
    assert len(result.failures) == 1
    assert result.total_time_ms > 0
    print(f"Processed {len(result.successes)} items in {result.total_time_ms:.0f}ms")
    print(f"Failures: {result.failures}")
```

---

## Part 3: Model Routing System

### Objective

Build a model routing system that classifies query complexity and routes to appropriate models.

### Requirements

1. Create a `ComplexityClassifier` that:
   - Analyzes query text for complexity signals
   - Returns complexity level (simple, medium, complex)
   - Uses multiple heuristics (length, keywords, patterns)

2. Create a `ModelRouter` that:
   - Maps complexity levels to models
   - Tracks routing statistics
   - Provides cost estimation

### Starter Code

```python
class ComplexityClassifier:
    SIMPLE_SIGNALS = ["what", "who", "when", "where", "how many", "define"]
    MEDIUM_SIGNALS = ["explain", "describe", "compare", "summarize", "list"]
    COMPLEX_SIGNALS = ["design", "implement", "analyze", "evaluate", "create a plan"]

    def classify(self, query: str) -> str:
        # TODO: Implement complexity classification
        # Consider: keywords, query length, presence of code/technical terms
        pass

class ModelRouter:
    MODEL_MAP = {
        "simple": "gpt-4o-mini",
        "medium": "gpt-4o-mini",
        "complex": "gpt-4o",
    }

    def __init__(self):
        self.routing_stats = {"simple": 0, "medium": 0, "complex": 0}

    def route(self, query: str) -> str:
        # TODO: Implement routing with stats tracking
        pass

    def estimate_cost(self, queries: list[str], avg_output_tokens: int = 100) -> dict:
        # TODO: Estimate total cost for a batch of queries
        pass
```

### Tests

```python
def test_model_router():
    router = ModelRouter()

    # Simple queries
    simple = ["What is Python?", "Who is Elon Musk?", "When was the internet invented?"]
    for q in simple:
        assert router.route(q) == "gpt-4o-mini"

    # Complex queries
    complex_queries = [
        "Design a scalable microservices architecture",
        "Implement a distributed consensus algorithm",
        "Evaluate the tradeoffs between SQL and NoSQL databases",
    ]
    for q in complex_queries:
        assert router.route(q) == "gpt-4o"

    print(f"Routing stats: {router.routing_stats}")

    # Cost estimation
    all_queries = simple + complex_queries
    cost = router.estimate_cost(all_queries, avg_output_tokens=150)
    print(f"Estimated cost: ${cost['total_cost']:.4f}")
```

---

## Part 4: Cost Optimization Measurement

### Objective

Build a cost measurement system that tracks and compares different optimization strategies.

### Requirements

1. Create a `CostAnalyzer` that:
   - Tracks token usage and costs per model
   - Compares costs across different strategies
   - Generates optimization reports

2. Implement comparison scenarios:
   - No optimization (all queries to expensive model)
   - Routing only
   - Caching only
   - Routing + caching combined

### Starter Code

```python
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class CostReport:
    strategy: str
    total_cost: float
    total_calls: int
    avg_cost_per_call: float
    model_breakdown: dict

class CostAnalyzer:
    MODEL_PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }

    def __init__(self):
        self.calls = []

    def record(self, model: str, input_tokens: int, output_tokens: int):
        # TODO: Record a model call
        pass

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        # TODO: Calculate cost for a single call
        pass

    def report(self, strategy_name: str) -> CostReport:
        # TODO: Generate report for recorded calls
        pass

    def compare(self, reports: list[CostReport]) -> dict:
        # TODO: Compare multiple strategy reports
        pass
```

### Tests

```python
def test_cost_analyzer():
    analyzer = CostAnalyzer()

    # Record some calls
    analyzer.record("gpt-4o", 500, 200)
    analyzer.record("gpt-4o", 1000, 500)
    analyzer.record("gpt-4o-mini", 200, 100)
    analyzer.record("gpt-4o-mini", 150, 50)

    report = analyzer.report("routing_only")
    assert report.total_calls == 4
    assert report.total_cost > 0
    assert report.avg_cost_per_call > 0

    print(f"Strategy: {report.strategy}")
    print(f"Total cost: ${report.total_cost:.4f}")
    print(f"Avg cost/call: ${report.avg_cost_per_call:.4f}")
    print(f"Model breakdown: {report.model_breakdown}")
```

---

## Bonus: Cost-Optimized RAG Pipeline

### Objective

Build a complete RAG pipeline with cost optimization including:
- Embedding caching
- Response caching
- Model routing
- Cost tracking

### Requirements

1. **Embedding Cache**: Cache embeddings to avoid recomputation
2. **Response Cache**: Cache LLM responses for repeated queries
3. **Model Router**: Route to appropriate models based on query complexity
4. **Cost Tracker**: Track all costs and generate reports
5. **Metrics**: Report cache hit rates, cost savings, and latency

### Architecture

```
User Query
    │
    ▼
┌─────────────┐
│ Query Cache │──hit──▶ Return cached response
└──────┬──────┘
       │ miss
       ▼
┌─────────────┐
│ Complexity  │
│ Classifier  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Model Router│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Embed Cache │──hit──▶ Use cached embedding
└──────┬──────┘
       │ miss
       ▼
┌─────────────┐
│ Embedding   │
│ Computation │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Vector      │
│ Search      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ LLM Call    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Cache Store │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Cost Track  │
└─────────────┘
```

### Evaluation Criteria

- All components work together
- Cost tracking is accurate
- Cache hit rates are reasonable (>30% for repeated queries)
- Model routing correctly identifies complexity
- System handles errors gracefully

---

## Submission

1. Complete all parts with working code
2. Include test results demonstrating functionality
3. Write a brief analysis of cost savings achieved
4. Bonus: Include a comparison chart of optimization strategies

## Resources

- `notebooks/01-caching-strategies.ipynb` — Caching implementation patterns
- `notebooks/02-batch-processing.ipynb` — Async processing examples
- `notebooks/03-cost-optimization.ipynb` — Model routing and cost tracking
- `resources.md` — Additional reference materials
