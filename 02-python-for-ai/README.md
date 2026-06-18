# Module 02: Python for AI

## Overview

This module provides a practical foundation in Python programming specifically tailored for AI engineering work. By the end of this module, you will be comfortable writing Python scripts, processing data with NumPy and Pandas, making API requests, and using Git for version control.

## Learning Objectives

- Write clean Python code using core language features
- Process and analyze data using NumPy and Pandas
- Make HTTP requests and parse JSON responses
- Use Git and GitHub for version control and collaboration

## Prerequisites

- Module 01: AI Fundamentals (or equivalent knowledge)
- Python 3.9+ installed on your system
- A code editor (VS Code recommended)
- Terminal / command line access

---

## 1. Python Basics for AI

Python is the dominant language in AI and machine learning due to its simplicity, readability, and massive ecosystem of libraries.

### 1.1 Variables and Data Types

Python is dynamically typed — you don't need to declare variable types explicitly.

```python
# Basic data types
name = "Alice"          # str
age = 30                # int
height = 5.7            # float
is_active = True        # bool

# Type checking
print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>
```

**Core data types in Python:**

| Type | Example | Use in AI |
|------|---------|-----------|
| `str` | `"hello"` | Text processing, NLP |
| `int` | `42` | Counters, indices |
| `float` | `3.14` | Weights, probabilities |
| `bool` | `True/False` | Flags, conditions |
| `list` | `[1, 2, 3]` | Sequences, batches |
| `dict` | `{"key": "val"}` | Configs, records |
| `tuple` | `(1, 2)` | Immutable sequences |

### 1.2 Lists

Lists are ordered, mutable sequences — the workhorse data structure in Python.

```python
# Creating lists
models = ["gpt-4", "claude-3", "gemini-pro"]
scores = [0.92, 0.87, 0.95]

# Indexing and slicing
print(models[0])        # "gpt-4"
print(scores[1:])       # [0.87, 0.95]

# Adding elements
models.append("llama-3")

# List comprehension (essential for AI work)
accuracies = [0.85, 0.92, 0.78, 0.96, 0.89]
good_models = [a for a in accuracies if a > 0.9]
# Result: [0.92, 0.96]

# Transform while filtering
model_scores = [(name, score) for name, score in zip(models, accuracies) if score > 0.9]
```

### 1.3 Dictionaries

Dictionaries map keys to values — used extensively for configuration, data records, and JSON-like structures.

```python
# Creating dictionaries
model_config = {
    "name": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 4096,
    "tools": ["code_interpreter", "retrieval"]
}

# Accessing values
print(model_config["temperature"])   # 0.7

# Safe access with .get()
api_key = model_config.get("api_key", "not_set")

# Dictionary comprehension
param_grid = {f"lr_{i}": 0.001 * (i + 1) for i in range(5)}
# Result: {'lr_0': 0.001, 'lr_1': 0.002, ...}

# Iterating
for key, value in model_config.items():
    print(f"{key}: {value}")
```

### 1.4 Conditionals and Loops

```python
# Conditional logic
accuracy = 0.88

if accuracy >= 0.95:
    grade = "excellent"
elif accuracy >= 0.85:
    grade = "good"
elif accuracy >= 0.70:
    grade = "acceptable"
else:
    grade = "needs improvement"

# Ternary operator
status = "pass" if accuracy >= 0.80 else "fail"

# For loops
training_losses = [0.5, 0.35, 0.22, 0.15, 0.11]
for epoch, loss in enumerate(training_losses):
    print(f"Epoch {epoch}: loss = {loss}")

# While loops (common in convergence checks)
loss = 1.0
epoch = 0
while loss > 0.01:
    loss *= 0.8  # simulated training
    epoch += 1
print(f"Converged after {epoch} epochs")
```

### 1.5 Functions

Functions are fundamental for reusable, testable code.

```python
# Basic function
def compute_accuracy(predictions, labels):
    """Compute classification accuracy."""
    correct = sum(1 for p, l in zip(predictions, labels) if p == l)
    return correct / len(labels)

# Default arguments
def train_model(dataset, epochs=10, lr=0.001, verbose=True):
    """Train a model with configurable parameters."""
    if verbose:
        print(f"Training on {dataset} for {epochs} epochs")
    # ... training logic ...
    return {"loss": 0.05, "accuracy": 0.94}

# *args and **kwargs
def log_metrics(*metrics, **options):
    """Log any number of metrics with optional formatting."""
    for m in metrics:
        print(f"Metric: {m}")
    for key, value in options.items():
        print(f"{key}: {value}")

log_metrics(0.92, 0.88, epoch=5, model="gpt-4")
```

### 1.6 Lambda Functions

Anonymous functions used for short operations, especially with `map`, `filter`, and `sorted`.

```python
# Lambda basics
square = lambda x: x ** 2
add = lambda x, y: x + y

# With sorted
models = [("gpt-4", 0.95), ("claude-3", 0.92), ("gemini", 0.89)]
sorted_models = sorted(models, key=lambda x: x[1], reverse=True)

# With map and filter
scores = [0.85, 0.92, 0.78, 0.96]
passed = list(filter(lambda s: s >= 0.80, scores))
doubled = list(map(lambda s: s * 2, scores))
```

### 1.7 File I/O

```python
# Writing to a file
with open("results.json", "w") as f:
    json.dump({"accuracy": 0.94, "loss": 0.05}, f)

# Reading from a file
with open("results.json", "r") as f:
    data = json.load(f)

# Reading line by line (for large files)
with open("large_dataset.txt", "r") as f:
    for line in f:
        process(line.strip())
```

---

## 2. Data Processing with NumPy and Pandas

### 2.1 NumPy — Numerical Computing

NumPy provides efficient array operations and is the foundation for nearly all numerical Python code.

```python
import numpy as np

# Array creation
arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros((3, 4))        # 3x4 matrix of zeros
ones = np.ones((2, 3))          # 2x3 matrix of ones
random = np.random.randn(5, 5)  # 5x5 random normal

# Array operations (vectorized — fast!)
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = a + b       # element-wise: [5, 7, 9]
d = a * b       # element-wise: [4, 10, 18]
e = np.dot(a, b)  # dot product: 32

# Slicing
matrix = np.random.randn(100, 5)
subset = matrix[0:10, :]       # first 10 rows, all columns
col_2 = matrix[:, 2]           # all rows, column 2

# Statistical operations
print(f"Mean: {matrix.mean()}")
print(f"Std: {matrix.std(axis=0)}")
print(f"Max: {matrix.max()}")
```

### 2.2 Pandas — Data Manipulation

Pandas provides DataFrames for structured data operations — think of it as Python's version of a spreadsheet.

```python
import pandas as pd

# Creating a DataFrame
data = {
    "model": ["gpt-4", "claude-3", "gemini-pro", "llama-3"],
    "accuracy": [0.95, 0.92, 0.89, 0.87],
    "latency_ms": [120, 95, 110, 200],
    "cost_per_1k": [0.03, 0.015, 0.01, 0.0]
}
df = pd.DataFrame(data)

# Reading from CSV
df = pd.read_csv("model_results.csv")

# Basic operations
print(df.head())          # First 5 rows
print(df.describe())      # Statistical summary
print(df.dtypes)          # Column types

# Filtering
fast_models = df[df["latency_ms"] < 150]
accurate_models = df[df["accuracy"] > 0.90]

# Multiple conditions
filtered = df[(df["accuracy"] > 0.90) & (df["cost_per_1k"] < 0.02)]

# Grouping and aggregation
summary = df.groupby("model").agg({
    "accuracy": "mean",
    "latency_ms": ["min", "max"]
})

# Adding new columns
df["efficiency"] = df["accuracy"] / df["latency_ms"]

# Handling missing values
df.fillna(0)                    # Fill with zero
df.dropna()                     # Remove rows with NaN
df["accuracy"].fillna(df["accuracy"].mean())  # Fill with mean

# Exporting
df.to_csv("processed_results.csv", index=False)
```

---

## 3. API Concepts and HTTP Requests

### 3.1 What is an API?

An API (Application Programming Interface) allows software applications to communicate over HTTP. In AI engineering, you'll use APIs to:

- Send prompts to LLMs (OpenAI, Anthropic, Google)
- Fetch training data from external sources
- Deploy models as web services
- Integrate with cloud platforms

### 3.2 HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `GET` | Retrieve data | Fetch weather, list models |
| `POST` | Send data | Submit prompt, create resource |
| `PUT` | Update data | Update configuration |
| `DELETE` | Remove data | Delete a resource |

### 3.3 JSON Format

JSON (JavaScript Object Notation) is the standard data format for APIs.

```json
{
  "model": "gpt-4",
  "response": {
    "text": "Hello, how can I help?",
    "tokens_used": 8
  },
  "metadata": {
    "latency_ms": 150,
    "status": "success"
  }
}
```

### 3.4 Making API Requests with Python

The `requests` library is the standard way to make HTTP requests in Python.

```python
import requests

# Simple GET request
response = requests.get("https://api.github.com/users/octocat")
data = response.json()
print(data["name"])

# POST request with JSON body
response = requests.post(
    "https://httpbin.org/post",
    json={"prompt": "Hello, world!", "max_tokens": 100}
)
print(response.json())

# Error handling
try:
    response = requests.get("https://api.example.com/data", timeout=10)
    response.raise_for_status()  # Raises exception for 4xx/5xx
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# Headers and authentication
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
response = requests.get("https://api.example.com/models", headers=headers)
```

### 3.5 Rate Limiting

APIs limit how many requests you can make in a given time period. Respect these limits:

- Check response headers for rate limit info (`X-RateLimit-Remaining`)
- Implement exponential backoff on failures
- Cache responses when possible
- Use batch endpoints instead of many individual requests

```python
import time

def make_request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 429:  # Rate limited
                wait = 2 ** attempt  # Exponential backoff
                print(f"Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

---

## 4. Git and GitHub Basics

### 4.1 Why Git?

Git tracks changes to your code, enabling:
- **Version history**: See what changed, when, and why
- **Collaboration**: Multiple people working on the same codebase
- **Experimentation**: Try new ideas in branches without breaking the main code
- **Backup**: Code is stored remotely on GitHub

### 4.2 Core Concepts

- **Repository (repo)**: A project folder tracked by Git
- **Commit**: A snapshot of your code at a point in time
- **Branch**: An independent line of development
- **Merge**: Combining branches together
- **Remote**: The version of your repo on GitHub
- **Clone**: Copying a remote repo to your local machine

### 4.3 Essential Commands

```bash
# Initialize a new repo
git init

# Clone an existing repo
git clone https://github.com/user/repo.git

# Check status
git status

# Stage files for commit
git add filename.py
git add .  # Stage all changes

# Commit with a message
git commit -m "Add data preprocessing module"

# Push to remote
git push origin main

# Pull latest changes
git pull origin main

# View history
git log --oneline

# Create and switch to a branch
git checkout -b feature/new-model

# Merge a branch
git checkout main
git merge feature/new-model
```

### 4.4 GitHub Workflow

1. **Clone** the repository
2. **Create** a feature branch
3. **Make** changes and commit
4. **Push** the branch to GitHub
5. **Open** a Pull Request
6. **Review** and merge

### 4.5 Commit Best Practices

- Write clear, concise commit messages
- Use the imperative mood ("Add feature" not "Added feature")
- Keep commits focused — one logical change per commit
- Reference issues when relevant ("Fix #42")

---

## Module Exercises

See the `exercises/` directory for hands-on practice.

- **Exercise 01**: Python fundamentals, Pandas operations, and API requests
- Inline exercises in each notebook

## Additional Resources

See `resources.md` for links to official documentation and tutorials.

## Next Module

**Module 03: AI Foundations** — Core machine learning concepts and your first models.
