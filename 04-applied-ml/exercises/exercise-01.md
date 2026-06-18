# Exercise 01: Applied Machine Learning & Model Evaluation

## Part 1: Train and Evaluate a Classifier

Using the Breast Cancer Wisconsin dataset (built into scikit-learn):

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
```

**Tasks:**

1. Load the dataset and examine its structure (features, target names, sample size)
2. Split into 80% train, 20% test with `random_state=42`
3. Train both a `RandomForestClassifier` (100 trees) and `LogisticRegression` (max_iter=1000)
4. Print classification reports for both models
5. Which model has better recall for malignant tumors? Why does recall matter more than accuracy here?
6. Plot confusion matrices for both models. What types of errors does each model make?

---

## Part 2: Diagnose Overfitting and Underfitting

Generate synthetic data:

```python
from sklearn.datasets import make_regression

X, y = make_regression(n_samples=100, n_features=1, noise=15, random_state=42)
```

**Tasks:**

1. Fit polynomial models of degree 1, 4, and 15
2. Compute training and test MSE for each
3. Plot learning curves for each model (use `learning_curve` from sklearn)
4. For each model, classify it as underfitting, overfitting, or good fit
5. Apply Ridge regression with `alpha=10` to the degree-15 model. How does the test MSE change?
6. Find the optimal alpha value using cross-validation

---

## Part 3: Precision vs. Recall Trade-offs

**Scenario analysis — for each scenario, answer: Should you optimize for precision or recall? Explain why.**

1. **Email spam detection**: A company wants to filter spam emails. What happens if legitimate emails go to spam (false positive)? What happens if spam reaches the inbox (false negative)?

2. **Medical screening for a rare disease** (1% prevalence): The test must identify as many sick patients as possible. What's the cost of a false positive? A false negative?

3. **Content moderation on a social media platform**: The platform must remove harmful content. Flagging innocent content (FP) causes user frustration. Missing harmful content (FN) causes reputational damage.

4. **Loan approval system**: The bank must predict whether applicants will default. What happens when a good applicant is rejected (FP)? What happens when a risky applicant is approved (FN)?

**For each scenario, write:**
- Precision or recall priority
- The cost of each error type (FP vs FN)
- A suggested classification threshold direction (above or below 0.5)

---

## Part 4: Analyze Data Bias

Examine the following dataset for potential bias:

```python
import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'age': np.random.normal(35, 10, n).clip(18, 70),
    'income': np.random.lognormal(10.5, 0.8, n),
    'education_years': np.random.poisson(14, n),
    'loan_approved': np.random.binomial(1, 0.6, n)
})

# Simulate bias: higher income → more likely approved
data['loan_approved'] = (data['income'] > data['income'].quantile(0.4)).astype(int)
```

**Tasks:**

1. Compute approval rates for different income quartiles
2. Is there a correlation between age and approval? Compute it
3. What type of bias does this dataset exhibit? (selection, label, measurement, or historical)
4. If you trained a model on this data, what不公平 outcomes might result?
5. Propose two techniques to mitigate this bias before training
6. How would you test whether your mitigation worked?

---

## Submission Guidelines

- For Parts 1 and 2: Write Python code in a notebook or script, run it, and report the results
- For Parts 3 and 4: Write analytical answers (text) with clear reasoning
- Document any difficulties encountered and how you resolved them
