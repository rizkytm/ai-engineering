# Module 06: Transformer Architecture & LLM Fundamentals

## Overview

This module covers the Transformer architecture — the backbone of modern NLP and Large Language Models. You'll learn how attention mechanisms work, how tokenization affects cost and performance, and how LLM inference actually generates text.

**Duration:** 4-5 hours  
**Prerequisites:** Module 01-05  

---

## Learning Objectives

By the end of this module, you will be able to:
- Explain how Transformers replaced RNNs and why they're superior
- Implement self-attention from scratch
- Understand tokenization algorithms (BPE, SentencePiece) and their cost implications
- Call LLM APIs and understand inference parameters
- Read model cards and identify model limitations

---

## 1. Evolution of NLP: From Bag-of-Words to Transformers

### 1.1 Bag-of-Words (BoW)

The simplest representation: count word frequencies, ignore order.

```python
# Bag of Words
text = "the cat sat on the mat"
vocabulary = ["the", "cat", "sat", "on", "mat"]
bow = [2, 1, 1, 1, 1]  # word counts
```

**Limitations:**
- No word order: "dog bites man" = "man bites dog"
- No semantic meaning: "good" and "excellent" treated as unrelated
- Sparse vectors: high dimensionality, mostly zeros

### 1.2 Word Embeddings

Dense vectors that capture semantic relationships.

```python
# Word2Vec-style embeddings
king - man + woman ≈ queen
```

**Improvement:** Words with similar meanings have similar vectors.  
**Still limited:** Each word gets ONE embedding regardless of context.

### 1.3 RNN/LSTM

Recurrent networks process sequences step-by-step, maintaining hidden state.

```
Input: "The cat sat on the mat"
Step 1: h1 = f("The", h0)
Step 2: h2 = f("cat", h1)
Step 3: h3 = f("sat", h2)
...
```

**Limitations:**
- Sequential processing: can't parallelize across time steps
- Vanishing gradients: hard to learn long-range dependencies
- Slow on long sequences: O(n) sequential operations

### 1.4 The Transformer Revolution

The 2017 paper "Attention Is All You Need" introduced a new architecture:
- **No recurrence:** processes all tokens in parallel
- **Self-attention:** directly models relationships between all positions
- **Scalable:** easy to scale to billions of parameters

---

## 2. Why Transformers Replaced RNNs

| Factor | RNN/LSTM | Transformer |
|--------|----------|-------------|
| Parallelization | Sequential (slow) | Parallel (fast) |
| Long-range dependencies | Limited by hidden state | Direct attention connections |
| Training speed | O(n) steps | O(1) parallel steps |
| Scalability | Hard to scale | Easily scales to billions |

### 2.1 Parallelization

RNNs must process tokens one at a time. Transformers process all tokens simultaneously.

```python
# RNN: sequential
hidden = torch.zeros(1, hidden_size)
for token in tokens:
    hidden, output = rnn(token, hidden)  # depends on previous step

# Transformer: parallel
embeddings = embedding_layer(tokens)  # all at once
attention_output = self_attention(embeddings)  # all positions attend to all others
```

### 2.2 Long-Range Dependencies

In RNNs, information must flow through hidden states across many steps:

```
"The cat, which was very fluffy and had soft orange fur, sat on the mat"
```

By the time the RNN reaches "sat", the connection to "cat" may be weak. Transformers connect every token directly to every other token.

---

## 3. Self-Attention Mechanism

### 3.1 Core Concept

Self-attention allows each token to "look at" every other token and compute a weighted combination based on relevance.

**Query (Q):** What am I looking for?  
**Key (K):** What do I contain?  
**Value (V):** What information do I provide?

### 3.2 Attention Calculation

```python
import numpy as np

def self_attention(Q, K, V):
    # Q, K, V shape: (seq_len, d_k)
    d_k = Q.shape[-1]
    
    # Compute attention scores
    scores = np.dot(Q, K.T) / np.sqrt(d_k)
    
    # Apply softmax to get weights
    weights = softmax(scores)
    
    # Weighted sum of values
    output = np.dot(weights, V)
    
    return output, weights
```

### 3.3 Why Scaling by √d_k?

Without scaling, large dimensionality leads to large dot products, pushing softmax into regions with tiny gradients. Scaling by √d_k keeps gradients stable.

---

## 4. Multi-Head Attention

Instead of one attention function, Transformers use multiple "heads" that attend to different aspects of the input.

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) * W_O

where head_i = Attention(Q * W_Qi, K * W_Ki, V * W_Vi)
```

**Benefits:**
- Different heads can focus on different relationships (syntactic, semantic, positional)
- Increases model capacity without increasing computation per head

---

## 5. Positional Encoding

Self-attention is permutation-invariant — it doesn't know token order. Positional encoding adds position information.

### 5.1 Sinusoidal Encoding (Original Transformer)

```
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

### 5.2 Learned Positional Embeddings (BERT, GPT)

Train position embeddings as parameters — model learns the best way to represent position.

---

## 6. Encoder-Decoder Architecture

### 6.1 Original Transformer (Seq2Seq)

```
Input → Encoder → Decoder → Output
                    ↑
              (cross-attention to encoder)
```

- **Encoder:** Processes input sequence, produces contextual representations
- **Decoder:** Generates output token by token, attending to encoder outputs

### 6.2 Encoder-Only: BERT

```
Input → Encoder → Output (all positions)
```

- Bidirectional: sees entire input
- Good for: classification, NER, question answering
- Trained with masked language modeling (predict hidden words)

### 6.3 Decoder-Only: GPT

```
Input → Decoder → Output (next token only)
```

- Autoregressive: generates tokens left-to-right
- Good for: text generation, code generation, conversation
- Trained with next-token prediction
- What most LLMs use today (GPT-4, LLaMA, Gemini)

---

## 7. What Are Large Language Models (LLMs)?

LLMs are transformer-based models trained on massive text corpora (trillions of tokens) to predict the next token.

### 7.1 Key Characteristics

- **Scale:** Billions of parameters (GPT-3: 175B, GPT-4: rumored 1.8T)
- **Emergent abilities:** Capabilities that appear at scale but not in smaller models
  - In-context learning: learning from examples in the prompt
  - Chain-of-thought reasoning
  - Instruction following
- **General purpose:** One model for many tasks via prompting

### 7.2 Training Pipeline

```
Stage 1: Pre-training (next token prediction on internet data)
    ↓
Stage 2: Supervised fine-tuning (SFT) on instruction-response pairs
    ↓
Stage 3: RLHF / RLAIF (aligning with human preferences)
```

---

## 8. Model Cards and Understanding Limitations

### 8.1 What's a Model Card?

A model card documents:
- **Architecture:** Type, size, layers, attention heads
- **Training data:** What data was used, size, language coverage
- **Performance:** Benchmarks, metrics
- **Limitations:** Known biases, failure modes, safety concerns
- **Ethical considerations:** Bias, toxicity, misinformation risks

### 8.2 Common Limitations

- **Hallucinations:** Confidently stating false information
- **Knowledge cutoff:** Training data has a cutoff date
- **Bias:** Reflects biases in training data
- **Math/logic:** Struggles with complex reasoning
- **Context window:** Limited input length
- **Cost:** Expensive to run at scale

### 8.3 How to Read a Model Card

Check: training data composition, benchmark results, known biases, intended use cases, and safety recommendations.

---

## 9. Tokenization

### 9.1 Why Tokenization?

LLMs process tokens, not raw text. Tokenization maps text to numerical IDs.

**Token ≠ Word:** One word may be multiple tokens, multiple words may be one token.

### 9.2 Byte-Pair Encoding (BPE)

1. Start with individual characters
2. Find most frequent adjacent pairs
3. Merge them into new tokens
4. Repeat until desired vocabulary size

```
"unhappiness" → ["un", "happy", "ness"] (3 tokens)
"the" → ["the"] (1 token)
"antidisestablishmentarianism" → ["anti", "dis", "establish", "ment", "arian", "ism"] (6 tokens)
```

### 9.3 SentencePiece

- Language-agnostic: works directly on raw text
- Treats input as unicode, not pre-tokenized
- Used by: LLaMA, T5, ALBERT

### 9.4 Tokenization Costs

| Text | Tokens (GPT-4) | Approx Cost |
|------|----------------|-------------|
| "Hello, world!" | 4 tokens | ~$0.0001 |
| 1 page of text | ~500 tokens | ~$0.01 |
| 1 novel (80k words) | ~100k tokens | ~$2.00 |

**Important:** API pricing is per token. Understanding tokenization helps control costs.

### 9.5 Context Window

Maximum tokens a model can process (input + output):
- GPT-3.5: 4,096 tokens
- GPT-4: 8,192 / 32,768 / 128,000 tokens
- Gemini 1.5: 1M+ tokens

---

## 10. LLM Inference: How Text Generation Works

### 10.1 Autoregressive Generation

LLMs generate text one token at a time, left to right:

```
Prompt: "The capital of France is"
Step 1: "The capital of France is" → predict "Paris"
Step 2: "The capital of France is Paris" → predict "."
Step 3: "The capital of France is Paris." → predict "<end>"
```

### 10.2 Sampling Strategies

**Greedy decoding:** Always pick the most probable token.  
- Pros: Deterministic, fast
- Cons: Repetitive, lacks creativity

**Temperature:** Controls randomness
```python
# Low temperature (0.1): very deterministic
# High temperature (2.0): very random, creative
probabilities = logits / temperature
```

**Top-p (nucleus sampling):** Only consider tokens whose cumulative probability exceeds p
```python
# top_p=0.9: only consider tokens in top 90% probability mass
```

**Top-k:** Only consider k most probable tokens

### 10.3 Streaming

Instead of waiting for the full response, stream tokens as they're generated:

```python
response = client.models.generate_content(
    model="gpt-4o-mini",
    contents=prompt,
    config=types.GenerateContentConfig(
        max_tokens=100,
        temperature=0.7,
        stream=True  # Stream tokens
    )
)
for chunk in response:
    print(chunk.text, end="", flush=True)
```

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| Attention | Each token attends to all others via Q, K, V |
| Multi-head | Multiple attention heads capture different relationships |
| Positional encoding | Adds order information to permutation-invariant attention |
| Encoder vs Decoder | BERT = encoder (understanding), GPT = decoder (generation) |
| Tokenization | Text → tokens, BPE/SentencePiece, affects cost |
| Inference | Autoregressive generation with sampling strategies |

---

## Practice

1. **notebooks/01-attention-mechanism.ipynb** — Implement self-attention in NumPy
2. **notebooks/02-tokenization.ipynb** — Explore tokenization and cost
3. **notebooks/03-llm-inference.ipynb** — Call OpenAI API and experiment with parameters
4. **exercises/exercise-01.md** — Hands-on practice problems
5. **resources.md** — Further reading and references

---

*Next Module: [Module 07: Prompt Engineering & In-Context Learning](../07-prompt-engineering/README.md)*
