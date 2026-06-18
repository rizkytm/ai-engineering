# Module 15: AI Observability — Resources

## Official Documentation

### LangSmith
- [LangSmith Documentation](https://docs.smith.langchain.com/) — Official docs for tracing, evaluation, and monitoring
- [LangSmith Quick Start](https://docs.smith.langchain.com/quickstart) — Get started in 5 minutes
- [Tracing Guide](https://docs.smith.langchain.com/tracing) — Comprehensive tracing documentation
- [Evaluation Guide](https://docs.smith.langchain.com/evaluation) — Automated evaluation patterns
- [LangSmith Python SDK](https://github.com/langchain-ai/langsmith-sdk/tree/main/python) — GitHub repository

### LangChain
- [LangChain Tracing](https://python.langchain.com/docs/langsmith) — LangChain + LangSmith integration
- [LangChain Callbacks](https://python.langchain.com/docs/modules/callbacks/) — Custom instrumentation
- [LangChain Ecosystem](https://python.langchain.com/docs/get_started/introduction) — Full framework docs

---

## LLMOps Resources

### Guides and Tutorials
- [LLMOps: The Complete Guide](https://www.anotherai.com/resources/llmops-the-complete-guide) — Comprehensive LLMOps overview
- [Productionizing LLMs](https://www.deeplearning.ai/the-batch/how-ais-are-putting-llms-into-production/) — DeepLearning.AI production guide
- [Building Reliable LLM Applications](https://docs.smith.langchain.com/concepts/reliability) — Reliability patterns

### Research Papers
- [Evaluating Large Language Models as Judges](https://arxiv.org/abs/2306.05685) — LLM-as-a-Judge research
- [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) — MT-Bench evaluation framework
- [A Survey on Hallucination in LLMs](https://arxiv.org/abs/2311.05232) — Understanding hallucinations

### Blog Posts
- [How We Built an AI-Powered Monitoring System](https://blog.langchain.dev/monitoring/) — Real-world implementation
- [Evaluating LLM Applications](https://blog.langchain.dev/evaluation/) — LangChain evaluation blog
- [Cost Optimization for LLM Applications](https://www.anthropic.com/news/cost-optimization) — Cost reduction strategies

---

## Evaluation Frameworks

### Automated Evaluation
- [RAGAS](https://docs.ragas.io/) — RAG evaluation framework
- [DeepEval](https://docs.confident-ai.com/) — LLM evaluation metrics
- [TruLens](https://truLens.org/) — Feedback functions and evaluations
- [LangSmith Evaluation](https://docs.smith.langchain.com/evaluation) — Built-in evaluation tools

### Metrics Libraries
- [NLTK](https://www.nltk.org/) — ROUGE, BLEU implementations
- [BERTScore](https://github.com/Tiiiger/bert_score) — Semantic similarity metrics
- [Hugging Face Evaluate](https://huggingface.co/docs/evaluate/) — Standardized evaluation metrics

---

## Monitoring and Observability Tools

### Commercial Platforms
- [LangSmith](https://smith.langchain.com/) — Full LLMOps platform
- [Helicone](https://helicone.ai/) — LLM proxy with monitoring
- [Braintrust](https://www.braintrustdata.com/) — AI evaluation platform
- [Arize AI](https://arize.com/) — ML observability
- [Weights & Biases](https://wandb.ai/) — Experiment tracking

### Open Source
- [Langfuse](https://langfuse.com/) — Open-source LLM engineering platform
- [Phoenix (Arize)](https://github.com/Arize-ai/phoenix) — Open-source observability
- [LitLLM](https://github.com/BerriAI/litellm) — LLM proxy with monitoring
- [OpenLLMetry](https://github.com/traceloop/openllmetry) — OpenTelemetry for LLMs

---

## Cost Management

### Pricing References
- [OpenAI Pricing](https://openai.com/pricing) — GPT model costs
- [Anthropic Pricing](https://www.anthropic.com/pricing) — Claude model costs
- [Google AI Pricing](https://ai.google.dev/pricing) — OpenAI model costs

### Optimization Strategies
- [Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching) — Reduce repeated token usage
- [Streaming](https://python.langchain.com/docs/modules/model_io/models/chat/streaming) — Improve perceived latency
- [Model Selection Guide](https://blog.langchain.dev/model-selection/) — Cost vs quality tradeoffs

---

## Community and Learning

### Courses and Workshops
- [LangChain Academy](https://academy.langchain.com/) — Official LangChain courses
- [DeepLearning.AI LangChain Course](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/) — LangChain fundamentals
- [AI Engineering Bootcamp](https://www.anotherai.com/) — Comprehensive AI engineering

### Communities
- [LangChain Discord](https://discord.gg/langchain) — Active community support
- [LangChain GitHub](https://github.com/langchain-ai) — Source code and issues
- [Reddit r/LangChain](https://www.reddit.com/r/LangChain/) — Community discussions

### Conferences and Events
- [LangChain Dev Day](https://www.langchain.dev/) — Annual conference
- [AI Engineer Summit](https://www.ai.engineering/) — AI engineering conference
- [NeurIPS](https://neurips.cc/) — ML research conference

---

## Tools and Libraries

### Tracing
```bash
pip install langsmith
pip install langfuse
pip install opentelemetry-api
```

### Evaluation
```bash
pip install ragas
pip install deepeval
pip install trulens-eval
pip install nltk
pip install bert-score
```

### Monitoring
```bash
pip install arize
pip import wandb
pip install litellm
```

---

## Best Practices Checklist

### Production Readiness
- [ ] Implement tracing for all LLM calls
- [ ] Set up cost monitoring and alerts
- [ ] Configure anomaly detection
- [ ] Establish evaluation baselines
- [ ] Create feedback collection mechanism
- [ ] Set up dashboards for key metrics
- [ ] Implement retry and fallback logic
- [ ] Document operational procedures

### Evaluation
- [ ] Define evaluation criteria for your use case
- [ ] Create test datasets with representative examples
- [ ] Implement automated evaluation pipelines
- [ ] Set up A/B testing for prompt changes
- [ ] Track evaluation metrics over time
- [ ] Regular model quality audits

### Cost Optimization
- [ ] Profile token usage patterns
- [ ] Implement prompt caching where applicable
- [ ] Consider model switching for different task complexities
- [ ] Monitor and set budget alerts
- [ ] Optimize prompt length without losing quality

---

## Quick Reference

### Key Metrics to Track
| Metric | Description | Target |
|--------|-------------|--------|
| Latency (p95) | 95th percentile response time | < 2s |
| Cost per request | Average cost per API call | Varies |
| Token usage | Average tokens consumed | Optimize |
| Accuracy | Task completion rate | > 90% |
| User satisfaction | Positive feedback ratio | > 80% |
| Hallucination rate | Fabricated information | < 5% |

### Monitoring Alerts
- Cost spike: > 2 standard deviations
- Latency degradation: > 50% increase
- Error rate: > 5% of requests
- Quality drop: < 70% accuracy

---

*Last updated: Module 15 - AI Observability*
