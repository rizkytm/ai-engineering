# Exercise 01: AI Observability Practice

## Overview

This exercise provides hands-on practice with AI observability tools and techniques. You'll set up tracing, build monitoring systems, create cost dashboards, and design evaluation pipelines.

**Estimated Time:** 2-3 hours

---

## Part 1: LangSmith Setup and Tracing

### Objective
Set up LangSmith for tracing a LangChain workflow and analyze the results.

### Instructions

1. **Create a LangSmith Account**
   - Go to [smith.langchain.com](https://smith.langchain.com)
   - Sign up for a free account
   - Generate an API key from Settings → API Keys

2. **Configure Environment**
   ```bash
   pip install langsmith langchain langchain-openai python-dotenv
   ```

   Create a `.env` file:
   ```
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your-api-key
   LANGCHAIN_PROJECT=exercise-project
   OPENAI_API_KEY=your-openai-key
   ```

3. **Build and Trace a Chain**
   Create a chain that:
   - Takes a topic as input
   - Generates 3 quiz questions about the topic
   - Evaluates each question for difficulty
   - Returns structured output

4. **Analyze Traces**
   - View the trace in LangSmith dashboard
   - Identify the total token usage
   - Find the slowest step
   - Note any errors or retries

### Deliverables
- Working LangSmith configuration
- Traced chain with at least 3 nested steps
- Screenshot or description of trace analysis

---

## Part 2: Build a Monitoring Wrapper

### Objective
Create a reusable monitoring wrapper for LLM API calls that tracks key metrics.

### Instructions

1. **Design the Wrapper Class**
   ```python
   class MonitoringWrapper:
       def __init__(self, llm, model_name: str):
           pass
       
       def invoke(self, messages: list) -> dict:
           # Track: latency, tokens, cost
           pass
       
       def get_metrics(self) -> dict:
           pass
       
       def export_metrics(self, filepath: str):
           pass
   ```

2. **Implement Cost Tracking**
   - Use the pricing table from the notebook
   - Calculate cost per request
   - Track cumulative cost

3. **Implement Latency Tracking**
   - Measure time to first token (TTFT)
   - Measure total generation time
   - Calculate percentiles (p50, p95, p99)

4. **Test the Wrapper**
   - Run 10 different queries
   - Generate a metrics report
   - Identify the most expensive query

### Requirements
- Must handle errors gracefully
- Must track metrics per-request
- Must support multiple models
- Must export metrics to JSON

### Deliverables
- Complete `MonitoringWrapper` class
- Test script with 10 queries
- Metrics report (JSON or printed summary)

---

## Part 3: Cost Tracking Dashboard

### Objective
Build a simple cost tracking dashboard that visualizes spending patterns.

### Instructions

1. **Create a CostTracker Class**
   ```python
   class CostTracker:
       def __init__(self):
           self.records = []
       
       def log_request(self, model, input_tokens, output_tokens, latency):
           pass
       
       def get_daily_summary(self) -> dict:
           pass
       
       def get_model_breakdown(self) -> dict:
           pass
       
       def detect_anomalies(self, threshold: float = 2.0) -> list:
           pass
   ```

2. **Generate Sample Data**
   - Create 100 simulated requests
   - Use different models (GPT-4, GPT-4o-mini)
   - Include some anomalies (high latency, high cost)

3. **Build Visualization**
   Create a function that generates:
   - Cost over time (line chart)
   - Cost by model (pie chart)
   - Latency distribution (histogram)
   - Anomaly highlights

   Use matplotlib or generate text-based charts.

4. **Implement Anomaly Detection**
   - Use z-score method
   - Flag requests with cost > 2 standard deviations
   - Flag requests with latency > 2 standard deviations

### Deliverables
- `CostTracker` class with all methods
- Visualization functions
- Anomaly detection results

---

## Part 4: RAG Evaluation Pipeline

### Objective
Design and implement an evaluation pipeline for a Retrieval-Augmented Generation (RAG) system.

### Instructions

1. **Design Evaluation Metrics**
   Create a `RAGEvaluator` class that evaluates:
   - **Answer Quality**: Relevance, accuracy, completeness
   - **Retrieval Quality**: Are relevant documents retrieved?
   - **Faithfulness**: Is the answer grounded in retrieved documents?
   - **Hallucination Rate**: Does the answer contain fabricated information?

2. **Build the Evaluator**
   ```python
   class RAGEvaluator:
       def __init__(self, judge_model: str = "gpt-4o"):
           pass
       
       def evaluate_answer(self, question, answer, context) -> dict:
           pass
       
       def evaluate_retrieval(self, question, retrieved_docs, ground_truth) -> dict:
           pass
       
       def calculate_hallucination_rate(self, answer, context) -> float:
           pass
       
       def run_evaluation(self, test_data: list) -> dict:
           pass
   ```

3. **Create Test Dataset**
   Create 10 test cases with:
   - Question
   - Expected answer (reference)
   - Retrieved documents
   - Actual RAG output

4. **Run and Analyze**
   - Run evaluation on all test cases
   - Calculate aggregate metrics
   - Identify common failure patterns
   - Suggest improvements

### Deliverables
- Complete `RAGEvaluator` class
- Test dataset (10 examples)
- Evaluation report with metrics and analysis

---

## Bonus: Build a Feedback Loop

### Objective
Create a feedback collection and analysis system that drives continuous improvement.

### Instructions

1. **Design the Feedback System**
   ```python
   class FeedbackLoop:
       def __init__(self):
           pass
       
       def collect_feedback(self, response_id, rating, comment=None):
           pass
       
       def analyze_patterns(self) -> dict:
           pass
       
       def generate_improvement_suggestions(self) -> list:
           pass
       
       def export_report(self, filepath):
           pass
   ```

2. **Implement Collection**
   - Support rating (1-5)
   - Support comments
   - Support tags (e.g., "inaccurate", "helpful")

3. **Implement Analysis**
   - Calculate satisfaction scores
   - Identify common complaints
   - Track sentiment over time
   - Correlate with metrics (cost, latency)

4. **Generate Suggestions**
   Based on analysis, generate actionable suggestions:
   - If accuracy is low → suggest RAG improvements
   - If latency is high → suggest model optimization
   - If cost is high → suggest model switching

### Deliverables
- Complete `FeedbackLoop` class
- Sample feedback data (20+ entries)
- Analysis report with improvement suggestions

---

## Submission

For each part, provide:
1. Working code (Python files or Jupyter notebooks)
2. Output/results (screenshots or text)
3. Brief explanation of your approach (1-2 paragraphs)

### Evaluation Criteria
- **Correctness**: Code works as intended
- **Completeness**: All requirements met
- **Code Quality**: Clean, well-organized code
- **Documentation**: Clear comments and explanations

---

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangChain Tracing Guide](https://python.langchain.com/docs/langsmith)
- [LLMOps Guide](https://www.anotherai.com/resources/llmops-the-complete-guide)
- [Evaluation Metrics](https://docs.smith.langchain.com/evaluation)

---

*Complete all parts to demonstrate mastery of AI observability concepts.*
