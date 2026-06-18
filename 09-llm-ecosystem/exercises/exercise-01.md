# Exercise 01: LLM Ecosystem & Hugging Face

## Prerequisites

- API keys for at least one provider (OpenAI, Anthropic, or Google)
- Hugging Face account (free): [huggingface.co](https://huggingface.co/)
- Python packages: `pip install transformers torch openai anthropic huggingface_hub pandas matplotlib`

Create a `.env` file:

```
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

---

## Part 1: Research and Compare 3 LLM Providers

### Objective

Build a structured comparison of three major LLM providers using real data.

### Instructions

1. Choose three providers from: OpenAI, Google, Anthropic, Meta, Mistral, DeepSeek
2. For each provider, find:
   - Available models and their context windows
   - Pricing per 1M tokens (input and output)
   - Rate limits (requests per minute, tokens per minute)
   - Notable strengths from their documentation
   - Model card highlights (training data cutoff, known limitations)
3. Create a comparison table:

| Factor | Provider 1 | Provider 2 | Provider 3 |
|--------|-----------|-----------|-----------|
| Best model | | | |
| Context window | | | |
| Input cost (per 1M tokens) | | | |
| Output cost (per 1M tokens) | | | |
| Rate limit | | | |
| Strengths | | | |
| Limitations | | | |

4. Write a 200-word recommendation: which provider would you choose for a customer service chatbot and why?

### Deliverables

- Comparison table with real data from provider documentation
- Written recommendation paragraph

---

## Part 2: Load and Use a Model from Hugging Face

### Objective

Load a model using the Hugging Face `pipeline` API and compare outputs across models.

### Instructions

1. Load a text-generation pipeline with Mistral-7B-Instruct:
   ```python
   from transformers import pipeline

   generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.3")
   ```

2. Generate responses to these prompts:
   - "What is the difference between supervised and unsupervised learning?"
   - "Write a Python function that checks if a string is a palindrome."
   - "Explain the concept of microservices in 3 sentences."

3. If Mistral-7B is too large for your hardware, use a smaller model:
   ```python
   generator = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
   ```

4. If you have an API key, also compare with a cloud model (GPT-4o-mini or Claude Haiku) on the same prompts.

5. Build a comparison table:

| Prompt | Mistral-7B Output Quality | Cloud Model Output Quality | Notes |
|--------|--------------------------|---------------------------|-------|
| Supervised vs unsupervised | | | |
| Palindrome function | | | |
| Microservices explanation | | | |

6. Answer these reflection questions:
   - Which model gave better explanations?
   - Which model wrote better code?
   - What differences did you notice in response style?

### Deliverables

- Python script or notebook that loads and runs models
- Comparison table with actual outputs
- Written reflection on differences

---

## Part 3: Build a Model Selection Decision Tree

### Objective

Create a decision tree that maps use cases to recommended LLMs.

### Instructions

1. Define these use cases:
   - Customer support chatbot
   - Document summarization for legal contracts
   - Code generation for internal tooling
   - Content marketing at scale (100K+ pieces/month)
   - Medical Q&A (requires HIPAA compliance)

2. For each use case, evaluate using these criteria:
   - Required quality level (1-5 scale)
   - Monthly token volume estimate
   - Budget constraint
   - Data privacy requirements (none / moderate / strict)
   - Latency requirement (< 1s / < 3s / < 10s)

3. Build a decision tree (text-based or drawn):

```
Is data privacy strict?
├── Yes → Self-hosted only
│   ├── High quality needed?
│   │   ├── Yes → Llama 3.1 70B or larger
│   │   └── No → Llama 3.1 8B or Mistral 7B
│   └── ...
└── No → API models available
    ├── High volume (> 50M tokens/month)?
    │   ├── Yes → Evaluate self-hosting vs API
    │   └── No → API models
    └── ...
```

4. Fill in your tree with specific model recommendations for each leaf node

5. Validate your tree against the 5 use cases — does each use case reach a reasonable recommendation?

### Deliverables

- Completed decision tree
- Validation showing each use case mapped through the tree

---

## Part 4: Cost Estimation for a Real-World Application

### Objective

Estimate monthly LLM costs for a realistic application.

### Scenario

You're building an AI assistant for a mid-size company (500 employees) that:
- Handles 5,000 chat conversations per day
- Average conversation: 10 messages back and forth
- Average message: 150 tokens input, 200 tokens output
- Also processes 200 document summaries per day (avg 5,000 tokens input, 500 tokens output)

### Instructions

1. Calculate total monthly tokens:
   - Chat: conversations × messages × tokens per message
   - Summaries: documents × (input + output tokens)
   - Total monthly = (chat + summaries) × 30 days

2. Estimate costs for three options:
   - **Option A:** GPT-4o-mini (cheap API)
   - **Option B:** Claude 3.5 Haiku (mid-tier API)
   - **Option C:** Self-hosted Llama 3.1 8B on a dedicated GPU

3. For Option C, estimate:
   - GPU cost (check cloud pricing: AWS, GCP, or Lambda Labs)
   - Engineering time for setup and maintenance (estimate hours × hourly rate)
   - Monthly operating cost

4. Create a cost comparison:

| Option | Monthly Token Cost | Infrastructure Cost | Engineering Cost | Total Monthly |
|--------|-------------------|--------------------|--------------------|---------------|
| GPT-4o-mini | | $0 | | |
| Claude Haiku | | $0 | | |
| Self-hosted Llama 3.1 8B | $0 | | | |

5. Make a recommendation with justification

### Deliverables

- Token calculation breakdown
- Cost comparison table
- Written recommendation (100 words)

---

## Bonus: Tokenizer Comparison

### Objective

Explore how different tokenizers affect token counts and cost.

### Instructions

1. Use the tiktoken library to count tokens for GPT-4:
   ```python
   import tiktoken
   enc = tiktoken.encoding_for_model("gpt-4")
   tokens = enc.encode("Your text here")
   print(f"Token count: {len(tokens)}, Tokens: {tokens}")
   ```

2. Use the transformers tokenizer for Llama 3:
   ```python
   from transformers import AutoTokenizer
   tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B")
   tokens = tokenizer.encode("Your text here")
   print(f"Token count: {len(tokens)}, Tokens: {tokens}")
   ```

3. Test with these inputs:
   - English paragraph (200 words)
   - Japanese paragraph (200 words)
   - Python function (50 lines)
   - JSON data structure

4. Build a comparison:

| Input | GPT-4 Tokens | Llama 3 Tokens | Cost Difference |
|-------|-------------|----------------|-----------------|
| English text | | | |
| Japanese text | | | |
| Python code | | | |
| JSON data | | | |

5. Calculate monthly cost difference for 50M tokens of each type

### Deliverables

- Token count comparison table
- Cost impact analysis
