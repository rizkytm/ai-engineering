# Module 05: Applied Deep Learning & The Road to Foundation Models

## Overview

This module bridges classical machine learning with modern deep learning and foundation models. You'll understand neural network fundamentals, text embeddings, and the Transformer architecture that powers today's large language models.

## Learning Objectives

By the end of this module, you will:

- Understand neural network structure and training mechanics
- Implement a simple neural network using PyTorch
- Convert text to numerical representations (embeddings)
- Understand why Transformers replaced RNNs and LSTMs
- Use pre-trained models via Hugging Face for inference
- Perform transfer learning and fine-tuning

---

## 1. Neural Network Structure

A neural network is a function approximator composed of layers of interconnected nodes (neurons).

### Architecture Components

```
Input Layer → Hidden Layer(s) → Output Layer
```

- **Input Layer**: Receives raw data. One neuron per feature (e.g., 784 pixels for MNIST).
- **Hidden Layers**: Intermediate layers that learn transformations. Each neuron applies a weighted sum + bias, then an activation function.
- **Output Layer**: Produces the final prediction. Number of neurons matches the task (e.g., 10 for 10-class classification).

### Weights and Biases

Each connection between neurons has a **weight** (w), and each neuron has a **bias** (b):

```
z = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
z = W·x + b
```

- **Weights** control the strength of connections
- **Biases** allow shifting the activation threshold
- Both are learned during training via gradient descent

### Activation Functions

Without activation functions, a neural network is just a linear model (linear composition = linear). Activation functions introduce **non-linearity**, allowing the network to learn complex patterns.

| Function | Formula | Range | Use Case |
|----------|---------|-------|----------|
| **ReLU** | max(0, x) | [0, ∞) | Hidden layers (default choice) |
| **Sigmoid** | 1 / (1 + e⁻ˣ) | (0, 1) | Binary output, gating |
| **Tanh** | (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ) | (-1, 1) | Hidden layers (less common now) |
| **Softmax** | eˣⁱ / Σeˣʲ | [0, 1], sums to 1 | Multi-class output |

---

## 2. Forward Propagation and Backpropagation

### Forward Propagation

Data flows from input to output, layer by layer:

```
Layer 1: h₁ = activation(W₁·x + b₁)
Layer 2: h₂ = activation(W₂·h₁ + b₂)
Output:  ŷ = softmax(W₃·h₂ + b₃)
```

Each layer transforms its input into a more abstract representation.

### Loss Function

Measures how wrong the prediction is:

- **Cross-Entropy Loss**: Standard for classification
- **MSE Loss**: Standard for regression

```
L(ŷ, y) = -Σ yᵢ · log(ŷᵢ)
```

### Backpropagation

The algorithm that computes gradients of the loss with respect to every weight in the network:

1. Compute loss from the output
2. Use the **chain rule** to propagate gradients backward layer by layer
3. Each weight's gradient tells us how much it contributed to the error

### Gradient Descent / Optimization

Update weights in the direction that reduces loss:

```
w_new = w_old - learning_rate × ∂L/∂w
```

Common optimizers:
- **SGD**: Basic gradient descent
- **Adam**: Adaptive learning rates (recommended default)

---

## 3. Training Loop

The standard training workflow:

```
For each epoch:
    For each batch:
        1. Forward pass → compute predictions
        2. Compute loss
        3. Backward pass → compute gradients
        4. Update weights
        5. Zero gradients
```

Key concepts:
- **Epoch**: One full pass through the entire training dataset
- **Batch**: A subset of data processed together (controls memory and gradient noise)
- **Learning rate**: How large the weight updates are

---

## 4. Text Embeddings: Turning Text into Numbers

Neural networks work with numbers, not words. **Embeddings** map discrete tokens (words, subwords) to dense continuous vectors.

### Why Embeddings Matter

| Method | Problem |
|--------|---------|
| **One-hot encoding** | Sparse, high-dimensional, no semantic meaning |
| **Bag-of-Words** | Loses word order, no context |
| **Word2Vec / GloVe** | Static embeddings, one vector per word regardless of context |
| **Contextual embeddings** | Different vectors for the same word in different contexts |

### How Embeddings Work

Modern embedding models (e.g., BERT, GPT) produce **contextual embeddings**:

```python
"bank" in "river bank" → [0.2, -0.8, 0.1, ...]
"bank" in "bank account" → [-0.5, 0.3, 0.7, ...]
```

The same word gets different vectors depending on surrounding context. These vectors capture **semantic meaning** — similar meanings produce similar vectors.

### Cosine Similarity

Measures how similar two vectors are by computing the cosine of the angle between them:

```
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
```

- Range: [-1, 1]
- 1 = identical direction (very similar)
- 0 = orthogonal (unrelated)
- -1 = opposite (dissimilar)

---

## 5. Limitations of RNN and LSTM

### Recurrent Neural Networks (RNNs)

RNNs process sequences by maintaining a hidden state that's updated at each time step:

```
hₜ = f(W·hₜ₋₁ + U·xₜ)
```

### The Problems

1. **Vanishing/Exploding Gradients**: Gradients shrink or grow exponentially over long sequences, making it hard to learn long-range dependencies.

2. **Sequential Processing**: Each step depends on the previous one — can't parallelize. This makes training slow on long sequences.

3. **Limited Memory**: Despite being "recurrent," RNNs struggle to remember information from more than ~50-100 tokens back.

4. **LSTMs Improved Memory** (but didn't solve everything):
   - Introduced gating mechanisms (forget gate, input gate, output gate)
   - Could learn longer-range dependencies (~200-500 tokens)
   - Still sequential, still slow to train

5. **No Attention Mechanism**: RNNs treat all input equally at each step. They can't selectively focus on relevant parts of the input.

---

## 6. Transformer Architecture and Self-Attention

The Transformer (Vaswani et al., 2017, "Attention Is All You Need") solved all of RNN's problems.

### Self-Attention Mechanism

The key innovation: **each token can directly attend to every other token**, regardless of distance.

```
Attention(Q, K, V) = softmax(QKᵀ / √dₖ) × V
```

- **Q (Query)**: What am I looking for?
- **K (Key)**: What do I contain?
- **V (Value)**: What information do I provide?
- The dot product QKᵀ computes relevance scores
- Scaled by √dₖ to prevent vanishing gradients in softmax

### Multi-Head Attention

Multiple attention "heads" learn different relationship types:
- Head 1 might capture syntactic relationships
- Head 2 might capture semantic relationships
- Head 3 might capture positional patterns

### Why Transformers Won

| RNN/LSTM | Transformer |
|----------|-------------|
| Sequential | Fully parallelizable |
| Long-range dependencies weak | Direct attention to any token |
| Slow training | Fast training (GPU-friendly) |
| Limited context window | Scalable context windows |

### Architecture Components

1. **Multi-Head Self-Attention**: Each position attends to all positions
2. **Feed-Forward Network**: Position-wise transformation
3. **Layer Normalization**: Stabilizes training
4. **Positional Encoding**: Injects sequence order information (since attention is order-agnostic)

---

## 7. Pre-trained Models and Transfer Learning

### Training from Scratch

- Requires massive datasets (billions of tokens)
- Requires enormous compute (weeks/months on GPU clusters)
- Cost: $1M-$100M+ for large models
- Practical only for well-funded labs

### Transfer Learning

Take a pre-trained model and adapt it to your task:

1. **Pre-training**: Model learns general language understanding from massive corpora (self-supervised: predict next word, fill masked tokens)
2. **Fine-tuning**: Update weights on your specific task's labeled data
3. **Inference**: Use the adapted model for predictions

### Fine-Tuning Approaches

| Approach | Description | Compute Cost |
|----------|-------------|-------------|
| **Full fine-tuning** | Update all parameters | High |
| **Feature extraction** | Freeze base, train new head | Low |
| **LoRA** | Low-rank adaptation of key layers | Medium |
| **Prompt engineering** | No training, just prompt design | None |

### Using Pre-trained Models (Hugging Face)

```python
from transformers import pipeline

# Sentiment analysis
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
# → [{'label': 'POSITIVE', 'score': 0.9998}]

# Text generation
generator = pipeline("text-generation", model="gpt2")
text = generator("The future of AI is", max_length=50)
```

### The Hugging Face Ecosystem

- **Model Hub**: 500K+ pre-trained models
- **Datasets**: 100K+ datasets for training
- **Transformers Library**: Standard API for all models
- **Tokenizers**: Fast, efficient text preprocessing
- **Accelerate**: Distributed training made easy

---

## Key Takeaways

1. Neural networks are universal function approximators — with enough data and capacity, they can learn almost any mapping
2. Backpropagation + gradient descent is how networks learn
3. Embeddings turn discrete text into continuous vectors that capture meaning
4. Transformers replaced RNNs by enabling parallel processing and direct long-range attention
5. Pre-trained models + transfer learning democratized deep learning — you don't need to train from scratch

---

## Next Steps

- **Notebook 01**: Build and train your first neural network in PyTorch
- **Notebook 02**: Explore text embeddings and semantic similarity
- **Notebook 03**: Use pre-trained Transformer models for inference
- **Exercise**: Practice end-to-end deep learning workflows
