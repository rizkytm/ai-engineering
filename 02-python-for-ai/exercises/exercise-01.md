# Exercise 01: Python for AI Practice

## Part 1: Python Fundamentals

### Exercise 1.1: List Comprehension

Write a list comprehension that generates the first 20 square numbers.

```python
# Your code here
squares = [???]
print(squares)
# Expected: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361]
```

---

### Exercise 1.2: Dictionary from Two Lists

Given two lists, create a dictionary mapping names to scores.

```python
names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
scores = [92, 87, 95, 78, 88]

# Your code here: create a dict called grade_book
grade_book = ???

print(grade_book)
# Expected: {'Alice': 92, 'Bob': 87, 'Charlie': 95, 'Diana': 78, 'Eve': 88}
```

---

### Exercise 1.3: Function with Default Args

Write a function `calculate_bmi(weight_kg, height_m, precision=2)` that:
- Calculates BMI using the formula: weight / height^2
- Returns the result rounded to `precision` decimal places
- Raises `ValueError` if height is 0 or negative

```python
# Your code here
def calculate_bmi(weight_kg, height_m, precision=2):
    ???

# Test cases
print(calculate_bmi(70, 1.75))       # Should print ~22.86
print(calculate_bmi(90, 2.0, 1))     # Should print 22.5
# calculate_bmi(70, 0)               # Should raise ValueError
```

---

### Exercise 1.4: *args and **kwargs

Write a function `flexible_add` that:
- Accepts any number of positional arguments (numbers) and adds them together
- Accepts an optional keyword argument `multiplier` (default 1) that multiplies the final sum

```python
# Your code here
def flexible_add(*args, multiplier=1):
    ???

# Test cases
print(flexible_add(1, 2, 3))              # Should print 6
print(flexible_add(1, 2, 3, multiplier=2)) # Should print 12
print(flexible_add(10, 20))               # Should print 30
```

---

### Exercise 1.5: Lambda + Sorting

Sort this list of dictionaries by `accuracy` (descending), then by `latency_ms` (ascending) as a tiebreaker.

```python
models = [
    {"name": "gpt-4", "accuracy": 0.95, "latency_ms": 120},
    {"name": "claude-3", "accuracy": 0.92, "latency_ms": 95},
    {"name": "gemini-pro", "accuracy": 0.92, "latency_ms": 110},
    {"name": "llama-3", "accuracy": 0.87, "latency_ms": 200},
    {"name": "mistral-7b", "accuracy": 0.84, "latency_ms": 85},
]

# Your code here: sort models
sorted_models = ???

for m in sorted_models:
    print(f"{m['name']}: {m['accuracy']} ({m['latency_ms']}ms)")
# Expected order: gpt-4, claude-3, gemini-pro, llama-3, mistral-7b
# (claude-3 before gemini-pro because same accuracy but lower latency)
```

---

## Part 2: Pandas Exercises

### Exercise 2.1: Create and Query a DataFrame

Create a DataFrame of AI models and answer questions about the data.

```python
import pandas as pd

data = {
    "model": ["gpt-4", "claude-3-opus", "gemini-pro", "llama-3-70b", "mistral-7b", "phi-3", "gemma-2"],
    "provider": ["openai", "anthropic", "google", "meta", "mistral", "microsoft", "google"],
    "params_b": [1800, 520, 440, 70, 7, 3.8, 9],
    "accuracy": [0.95, 0.93, 0.89, 0.88, 0.84, 0.82, 0.86],
    "open_source": [False, False, False, True, True, True, True],
    "cost_per_1k": [0.03, 0.015, 0.01, 0.0, 0.005, 0.002, 0.0]
}

df = pd.DataFrame(data)
```

**Questions:**

1. Filter for open-source models with accuracy > 0.85
2. Find the average number of parameters by provider
3. Which model has the best accuracy-to-cost ratio?
4. Create a new column `tier` based on accuracy: >= 0.90 = "top", >= 0.85 = "mid", else = "base"

```python
# Your answers here:
```

---

### Exercise 2.2: GroupBy and Aggregation

Using this sales data:

```python
import numpy as np

np.random.seed(42)
n = 200

sales = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=n, freq="D"),
    "region": np.random.choice(["North", "South", "East", "West"], n),
    "product": np.random.choice(["API Calls", "Fine-tuning", "Consulting"], n),
    "revenue": np.random.exponential(5000, n).round(2),
    "units": np.random.randint(1, 50, n)
})
```

Write code to answer:

1. What is the total revenue by region?
2. What is the average revenue per unit for each product?
3. Which region has the highest average daily revenue?
4. What are the top 5 revenue days?

---

## Part 3: API Exercise

### Exercise 3.1: Fetch and Analyze Data

Using the JSONPlaceholder API (`https://jsonplaceholder.typicode.com`):

1. Fetch all posts and all users
2. Create a DataFrame with columns: post_id, title, author_name, author_email
3. Find which author wrote the most posts
4. Calculate the average title length by author

```python
import requests
import pandas as pd

# Your code here
```

---

### Exercise 3.2: Error Handling

Write a function that attempts to fetch data from a URL with:
- A timeout of 5 seconds
- Retries up to 3 times on failure
- Proper error messages for different failure types

```python
# Your code here
def robust_fetch(url, max_retries=3, timeout=5):
    ???
```

---

## Bonus: Combined Exercise

Write a complete script that:

1. Creates a CSV file with 50 synthetic model evaluation records (model name, task, accuracy, latency, tokens, cost)
2. Reads the CSV back with Pandas
3. Finds the best model per task
4. Fetches the top 5 posts from JSONPlaceholder
5. Saves a summary report to `report.txt`

```python
# Your code here
```

---

## Solutions

<details>
<summary>Click to expand solutions (attempt exercises first!)</summary>

### 1.1 Solution
```python
squares = [x ** 2 for x in range(20)]
```

### 1.2 Solution
```python
grade_book = dict(zip(names, scores))
```

### 1.3 Solution
```python
def calculate_bmi(weight_kg, height_m, precision=2):
    if height_m <= 0:
        raise ValueError("Height must be positive")
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, precision)
```

### 1.4 Solution
```python
def flexible_add(*args, multiplier=1):
    return sum(args) * multiplier
```

### 1.5 Solution
```python
sorted_models = sorted(models, key=lambda m: (-m["accuracy"], m["latency_ms"]))
```

### 2.1 Solution
```python
# 1. Open source with accuracy > 0.85
result = df[(df["open_source"] == True) & (df["accuracy"] > 0.85)]

# 2. Average params by provider
df.groupby("provider")["params_b"].mean()

# 3. Best accuracy-to-cost ratio
df.assign(ratio=lambda x: x["accuracy"] / x["cost_per_1k"].clip(lower=0.001)).sort_values("ratio", ascending=False).head(1)

# 4. Add tier column
df["tier"] = pd.cut(df["accuracy"], bins=[0, 0.85, 0.90, 1.0], labels=["base", "mid", "top"])
```

</details>
