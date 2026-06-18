# Module 15: AI Observability — Monitoring & Evaluation

## Overview

Observability is the backbone of production AI systems. Unlike traditional software with deterministic outputs, AI applications produce non-deterministic responses that require specialized monitoring, evaluation, and feedback mechanisms. This module covers LLMOps practices, metrics tracking, and automated evaluation for AI pipelines.

## Learning Objectives

By the end of this module, you will be able to:

- Set up and configure LangSmith for AI pipeline tracing
- Monitor key metrics: latency, token usage, cost, accuracy, user satisfaction
- Debug AI pipeline bottlenecks using trace analysis
- Implement cost monitoring and anomaly detection
- Build automated evaluation pipelines using LLM-as-a-Judge
- Design feedback loops for continuous improvement

---

## 1. LLMOps and Why Observability Matters for AI

### What is LLMOps?

LLMOps (Large Language Model Operations) encompasses the practices, tools, and infrastructure needed to deploy, monitor, and maintain LLM-based applications in production. It extends MLOps with specific considerations for generative AI:

- **Prompt management** — versioning and testing prompts
- **Chain observability** — tracing multi-step LLM workflows
- **Token-level monitoring** — tracking usage and costs
- **Output quality tracking** — evaluating non-deterministic responses
- **Feedback integration** — incorporating human and automated evaluations

### Why Traditional Monitoring Falls Short

Traditional software monitoring relies on deterministic outputs and well-defined error codes. AI systems introduce unique challenges:

| Traditional Software | AI Applications |
|---------------------|-----------------|
| Deterministic outputs | Non-deterministic responses |
| Binary success/failure | Gradual quality degradation |
| Fixed latency patterns | Variable token-based latency |
| Clear error boundaries | Ambiguous failure modes |
| Static inputs | Dynamic, unpredictable inputs |

### The Observability Stack

```
┌─────────────────────────────────────────────┐
│              User Interface                 │
├─────────────────────────────────────────────┤
│           Application Layer                 │
├─────────────────────────────────────────────┤
│         LLM Chain / Pipeline                │
├─────────────┬──────────────┬────────────────┤
│  LangSmith  │   Custom     │   External     │
│  Tracing    │   Metrics    │   Evaluation   │
├─────────────┴──────────────┴────────────────┤
│           Data Storage & Analytics          │
└─────────────────────────────────────────────┘
```

---

## 2. Monitoring AI vs Traditional Software

### Non-Deterministic Outputs

The same prompt can produce different responses across runs. This requires:

- **Response comparison** — evaluating quality across multiple runs
- **Consistency tracking** — measuring output stability
- **Semantic similarity** — comparing meaning, not exact text

### Unique AI Metrics

#### Latency
- **Time to First Token (TTFT)** — responsiveness for streaming
- **Total Generation Time** — end-to-end response time
- **Chain Execution Time** — time spent in multi-step pipelines

#### Token Usage
- **Input tokens** — prompt and context length
- **Output tokens** — response length
- **Total tokens** — combined usage per request
- **Token efficiency** — useful output per token consumed

#### Cost
- **Per-request cost** — based on model pricing
- **Daily/weekly/monthly spend** — budget tracking
- **Cost per quality unit** — cost divided by evaluation score
- **Cost anomalies** — unexpected spikes in usage

#### Accuracy & Quality
- **Task completion rate** — percentage of successful outcomes
- **Relevance scores** — how well responses address the query
- **Factual accuracy** — correctness of generated content
- **Hallucination rate** — frequency of fabricated information

#### User Satisfaction
- **Explicit feedback** — thumbs up/down, ratings
- **Implicit signals** — rephrasing, abandonment, regeneration
- **Session duration** — engagement metrics
- **Retention rates** — return user patterns

---

## 3. LangSmith Setup and Integration

### Account Setup

1. Create a LangSmith account at [smith.langchain.com](https://smith.langchain.com)
2. Generate an API key from Settings → API Keys
3. Install the LangSmith SDK:

```bash
pip install langsmith
```

### Configuration

```python
import os
from langsmith import Client

# Set environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "your-project-name"
```

### Integration with LangChain

LangChain automatically integrates with LangSmith when environment variables are set:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Create components
llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms"
)
parser = StrOutputParser()

# Chain automatically traced when LANGCHAIN_TRACING_V2=true
chain = prompt | llm | parser
result = chain.invoke({"topic": "machine learning"})
```

---

## 4. Trace Analysis

### Understanding Trace Structure

A trace in LangSmith captures the complete execution flow:

```
Trace (run)
├── Run: prompt template
│   └── Input: {topic: "machine learning"}
├── Run: ChatOpenAI
│   ├── Input: [messages]
│   ├── Output: response
│   ├── Tokens: input=15, output=150
│   └── Latency: 1.2s
├── Run: StrOutputParser
│   ├── Input: AIMessage
│   └── Output: "Machine learning is..."
└── Output: "Machine learning is..."
```

### Prompt → Chain → Tool Call → Response

Tracing reveals the full pipeline execution:

```python
# Example with tool usage
from langchain.agents import create_tool_calling_agent
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

# The trace will show:
# 1. Prompt construction
# 2. LLM call with tool options
# 3. Tool selection and execution
# 4. Tool result processing
# 5. Final LLM response
```

### Visual Debugging

LangSmith provides visual pipeline views that help identify:

- **Bottlenecks** — which steps take the longest
- **Token-heavy operations** — where tokens are consumed
- **Error points** — where failures occur
- **Retry patterns** — repeated LLM calls

---

## 5. Cost Monitoring and Anomaly Detection

### Cost Tracking Implementation

```python
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class CostRecord:
    timestamp: float
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    latency_ms: float
    metadata: Optional[dict] = None

class CostMonitor:
    def __init__(self):
        self.records: list[CostRecord] = []
    
    def log_request(self, model: str, input_tokens: int, 
                    output_tokens: int, latency_ms: float):
        # Pricing per 1M tokens (example: GPT-4)
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
        }
        
        model_pricing = pricing.get(model, pricing["gpt-4"])
        cost = (input_tokens * model_pricing["input"] + 
                output_tokens * model_pricing["output"]) / 1_000_000
        
        record = CostRecord(
            timestamp=time.time(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            latency_ms=latency_ms
        )
        self.records.append(record)
        return record
    
    def get_daily_cost(self) -> float:
        today = time.time() - 86400
        return sum(r.cost_usd for r in self.records if r.timestamp > today)
```

### Anomaly Detection

```python
import statistics

class AnomalyDetector:
    def __init__(self, window_size: int = 100, threshold: float = 2.0):
        self.window_size = window_size
        self.threshold = threshold
        self.cost_history: list[float] = []
    
    def check_anomaly(self, cost: float) -> bool:
        if len(self.cost_history) < self.window_size:
            self.cost_history.append(cost)
            return False
        
        mean = statistics.mean(self.cost_history)
        stdev = statistics.stdev(self.cost_history)
        
        is_anomaly = abs(cost - mean) > self.threshold * stdev
        
        self.cost_history.append(cost)
        if len(self.cost_history) > self.window_size:
            self.cost_history.pop(0)
        
        return is_anomaly
```

---

## 6. Automated Evaluation

### LLM-as-a-Judge

Using an LLM to evaluate outputs from another LLM:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

judge_prompt = ChatPromptTemplate.from_template("""
You are an expert evaluator. Rate the following response on a scale of 1-5.

Question: {question}
Response: {response}

Evaluation criteria:
1. Relevance: Does it address the question?
2. Accuracy: Is the information correct?
3. Clarity: Is it easy to understand?
4. Completeness: Does it cover the topic?

Provide your rating (1-5) and brief explanation.
""")

def llm_judge(question: str, response: str) -> dict:
    llm = ChatOpenAI(model="gpt-4")
    chain = judge_prompt | llm
    result = chain.invoke({"question": question, "response": response})
    # Parse rating from response
    return {"rating": parse_rating(result.content), "explanation": result.content}
```

### Evaluation Metrics

#### Automated Metrics
- **ROUGE/BLEU** — text overlap with reference
- **BERTScore** — semantic similarity
- **Faithfulness** — grounded in context
- **Relevance** — addresses the query

#### Human Evaluation Integration
```python
def collect_feedback(response_id: str, rating: int, comment: str):
    """Store human feedback for analysis."""
    feedback = {
        "response_id": response_id,
        "rating": rating,
        "comment": comment,
        "timestamp": time.time()
    }
    # Store in database
    return feedback
```

---

## 7. Feedback Loops for Continuous Improvement

### Feedback Loop Architecture

```
┌─────────────────────────────────────────────────┐
│                  Production                     │
│  User Query → LLM → Response → User Feedback   │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              Data Collection                    │
│  Traces + Metrics + Human Feedback             │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              Analysis & Evaluation              │
│  Automated Scoring + Pattern Detection         │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              Improvement Actions                │
│  Prompt Tuning + Model Selection + Fine-tuning │
└─────────────────────────────────────────────────┘
```

### Continuous Improvement Strategies

1. **Prompt Optimization** — refine based on low-scoring outputs
2. **Model Selection** — switch models based on cost/quality tradeoffs
3. **Fine-tuning** — train on high-quality examples
4. **RAG Enhancement** — improve retrieval based on relevance scores
5. **Guardrails** — add filters for common failure modes

---

## Key Takeaways

1. AI observability requires specialized tools and metrics beyond traditional monitoring
2. LangSmith provides comprehensive tracing for LangChain applications
3. Cost monitoring is critical for production AI systems
4. LLM-as-a-Judge enables scalable automated evaluation
5. Feedback loops drive continuous improvement in AI quality

## Next Steps

- Complete the hands-on notebooks in this module
- Practice with the exercises to reinforce concepts
- Explore the resources for deeper LLMOps knowledge

---

## Navigation

**Previous:** [Module 14: AI Governance](../14-governance/)  
**Next:** [Module 16: AI Economics](../16-economics/)

---

*This module is part of the AI Engineering curriculum. For questions and support, refer to the course repository.*
