# Exercise 01 — Transformer Architecture & LLM Fundamentals

## Part 1: Implement Self-Attention in Pure Python

### Task

Implement a self-attention function from scratch without using any ML libraries (no PyTorch, TensorFlow, or NumPy for the attention computation itself — only for verification).

### Requirements

```python
def self_attention(Q, K, V):
    """
    Compute self-attention.
    
    Args:
        Q: Query matrix (seq_len, d_k) - list of lists
        K: Key matrix (seq_len, d_k) - list of lists
        V: Value matrix (seq_len, d_v) - list of lists
    
    Returns:
        output: Attention output (seq_len, d_v) - list of lists
        weights: Attention weights (seq_len, seq_len) - list of lists
    """
```

### Steps

1. **Implement softmax** — write your own softmax function that works on a list of numbers
2. **Compute dot product** — implement matrix multiplication for Q @ K.T
3. **Scale** — divide by √d_k
4. **Apply softmax** — row-wise softmax to get attention weights
5. **Weighted sum** — multiply weights by V

### Test Case

```python
# Simple test
Q = [[1, 0], [0, 1]]
K = [[1, 0], [0, 1]]
V = [[1, 2], [3, 4]]

output, weights = self_attention(Q, K, V)
print("Weights:", weights)
print("Output:", output)
# Expected: weights should be identity-like, output should equal V
```

### Verify

Compare your output against NumPy implementation:

```python
import numpy as np

Q_np = np.array(Q)
K_np = np.array(K)
V_np = np.array(V)

d_k = Q_np.shape[-1]
scores = np.dot(Q_np, K_np.T) / np.sqrt(d_k)
weights_np = np.exp(scores) / np.exp(scores).sum(axis=-1, keepdims=True)
output_np = np.dot(weights_np, V_np)
```

---

## Part 2: Tokenize and Compare Different Texts

### Task

Analyze how different types of text tokenize and their cost implications.

### Instructions

1. Use `tiktoken` with the `cl100k_base` encoding (GPT-4 tokenizer)
2. Tokenize the following texts and record token counts:

```python
texts = {
    "English": "The quick brown fox jumps over the lazy dog.",
    "Code": "def fibonacci(n):\n    if n < 2:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
    "JSON": '{"name": "Alice", "age": 30, "skills": ["python", "ml", "nlp"]}',
    "URL": "https://api.example.com/v2/users?limit=100&offset=200",
    "Emoji": "I love coding! 🎉🚀💻",
    "Repetitive": "the the the the the the the the the the the",
}
```

3. For each text, calculate:
   - Number of characters
   - Number of tokens
   - Characters per token ratio
   - Estimated cost at $30/1M input tokens (GPT-4 pricing)

4. Answer: Which text type is most token-efficient? Why?

---

## Part 3: Experiment with LLM Parameters

### Task

Use the OpenAI API (or any LLM API you have access to) to observe how parameters affect output.

### Experiments

**Experiment 3a: Temperature Sweep**

Run the same prompt 10 times each at temperatures 0.0, 0.5, 1.0, and 2.0:

```python
prompt = "Give me 3 creative names for a space exploration game."
```

Record:
- How many unique responses did you get at each temperature?
- Which temperature gives the most consistent results?
- Which temperature gives the most creative results?

**Experiment 3b: Top-p Impact**

Compare outputs with:
- temperature=1.0, top_p=0.1 (very conservative)
- temperature=1.0, top_p=0.5 (moderate)
- temperature=1.0, top_p=0.9 (diverse)
- temperature=1.0, top_p=1.0 (full distribution)

**Experiment 3c: Max Tokens**

Test with max_output_tokens = 10, 50, 100, 500:

```python
prompt = "Explain quantum entanglement."
```

At what point does the response feel complete vs. truncated?

---

## Part 4: Cost Estimation Exercise

### Task

Build a cost estimator for a chatbot application.

### Requirements

Create a function `estimate_conversation_cost()` that:

1. Takes a list of messages (user + assistant turns)
2. Tokenizes each message
3. Calculates cost for different models:

| Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) |
|-------|----------------------------|------------------------------|
| GPT-4 | $30.00 | $60.00 |
| GPT-4 Turbo | $10.00 | $30.00 |
| GPT-3.5 Turbo | $0.50 | $1.50 |
| Gemini 1.5 Flash | $0.075 | $0.30 |
| Gemini 1.5 Pro | $1.25 | $5.00 |

### Test Data

```python
conversation = [
    {"role": "system", "content": "You are a helpful customer support agent for a tech company."},
    {"role": "user", "content": "My laptop won't turn on. I've tried holding the power button for 30 seconds."},
    {"role": "assistant", "content": "I understand you're having trouble with your laptop. Let's try a few troubleshooting steps: 1) Make sure the power adapter is firmly connected..."},
    {"role": "user", "content": "I tried that but the charging light isn't coming on either."},
    {"role": "assistant", "content": "That suggests the issue might be with the power adapter or the charging port. Can you try a different outlet?"},
]
```

### Expected Output

```
Conversation Cost Estimate
==========================

Model               Input Cost    Output Cost    Total Cost
GPT-4               $0.00450      $0.00180       $0.00630
GPT-4 Turbo         $0.00150      $0.00090       $0.00240
GPT-3.5 Turbo       $0.00012      $0.00009       $0.00021
Gemini 1.5 Flash    $0.00002      $0.00002       $0.00004
Gemini 1.5 Pro      $0.00060      $0.00040       $0.00100

Total tokens in conversation: 150 (input: 100, output: 50)
```

### Bonus

Estimate monthly cost for:
- 10,000 conversations/day
- Average 5 turns per conversation
- Average 50 tokens per turn

---

## Submission

Complete all 4 parts and submit:

1. Part 1: Your self-attention implementation + test results
2. Part 2: Tokenization analysis table + answer to the efficiency question
3. Part 3: Parameter experiment observations
4. Part 4: Cost estimator code + monthly cost estimate

Save your work as a single notebook or Python file and share the results.
