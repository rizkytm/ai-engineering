# Module 04: Applied Machine Learning & Model Evaluation

## Overview

Machine learning (ML) is the practice of building systems that learn patterns from data and make predictions or decisions without being explicitly programmed for each scenario. This module covers the fundamentals of ML, practical model building, and rigorous evaluation techniques.

## Learning Objectives

- Understand the types of ML: supervised, unsupervised, and reinforcement learning
- Build and train models using scikit-learn
- Evaluate models using appropriate metrics
- Recognize and handle overfitting, underfitting, and data bias
- Make informed precision vs. recall trade-offs for business applications

---

## 1. What is Machine Learning?

Machine learning models identify patterns in data and use those patterns to make predictions on new, unseen data.

**Core idea:** Instead of writing rules manually, you feed data to an algorithm that learns the rules automatically.

```
Traditional Programming:  Data + Rules → Output
Machine Learning:         Data + Output → Rules (Model)
```

### Types of Machine Learning

#### Supervised Learning
The model learns from **labeled data** — each example has an input and a known correct output.

- **Classification:** Predict a category (e.g., spam vs. not spam, tumor malignant vs. benign)
- **Regression:** Predict a continuous value (e.g., house price, temperature)

#### Unsupervised Learning
The model finds structure in **unlabeled data** — no predefined correct answers.

- **Clustering:** Group similar data points (e.g., customer segmentation)
- **Dimensionality Reduction:** Simplify data by reducing features while preserving structure (e.g., PCA)

#### Reinforcement Learning
An agent learns by interacting with an environment, receiving rewards or penalties for its actions. Used in robotics, game playing, and autonomous systems. We'll cover this conceptually — deep RL is an advanced topic.

---

## 2. Training vs. Inference

| Phase | What Happens | When |
|-------|--------------|------|
| **Training** | Model learns patterns from training data by minimizing a loss function | During development |
| **Inference** | Trained model makes predictions on new data | In production |

Training is computationally expensive (GPU, hours/days). Inference must be fast (milliseconds per prediction).

---

## 3. Data Splits

You **never** evaluate a model on data it has seen during training. Standard practice:

- **Training set (60-80%):** Used to fit the model
- **Validation set (10-20%):** Used to tune hyperparameters and select the best model
- **Test set (10-20%):** Held out until the very end; used for final performance estimation

```python
from sklearn.model_selection import train_test_split

# First split: separate test set
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Second split: separate validation from training
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.25, random_state=42
)
# Result: 60% train, 20% val, 20% test
```

---

## 4. Overfitting, Underfitting, and Generalization

| Problem | Symptom | Cause | Fix |
|---------|---------|-------|-----|
| **Underfitting** | Poor performance on training AND test data | Model too simple | Add features, use more complex model, train longer |
| **Overfitting** | Great training performance, poor test performance | Model memorizes noise | More data, regularization, simpler model, early stopping |
| **Good generalization** | Similar performance on training AND test data | Appropriate complexity | The goal |

**Generalization** is the ability to perform well on unseen data. A model that generalizes captures the true underlying pattern without memorizing noise.

---

## 5. Classification Metrics

### Confusion Matrix

For binary classification (positive/negative):

```
                    Predicted
                  Neg       Pos
Actual Neg    [ TN    |   FP   ]
Actual Pos    [ FN    |   TP   ]
```

- **True Positive (TP):** Correctly predicted positive
- **True Negative (TN):** Correctly predicted negative
- **False Positive (FP):** Incorrectly predicted positive (Type I error)
- **False Negative (FN):** Incorrectly predicted negative (Type II error)

### Key Metrics

| Metric | Formula | Best For |
|--------|---------|----------|
| **Accuracy** | (TP + TN) / Total | Balanced classes |
| **Precision** | TP / (TP + FP) | When false positives are costly |
| **Recall (Sensitivity)** | TP / (TP + FN) | When false negatives are costly |
| **F1-Score** | 2 × (Precision × Recall) / (Precision + Recall) | Imbalanced classes, balance precision and recall |

### Precision vs. Recall Trade-off

This is one of the most important decisions in applied ML:

**High Precision (minimize false positives):**
- Spam filter: You don't want legitimate emails in spam
- Content recommendation: Wrong recommendations annoy users
- Legal document review: False positives waste lawyer time

**High Recall (minimize false negatives):**
- Medical diagnosis: Missing a disease is worse than a false alarm
- Fraud detection: Missing fraud costs real money
- Safety systems: Missing a threat can be catastrophic

**You can't maximize both simultaneously** — improving one typically degrades the other. The threshold for classification (default 0.5) can be tuned to favor precision or recall based on business needs.

---

## 6. Data Bias and Model Limitations

### Data Bias
- **Selection bias:** Training data doesn't represent the real population
- **Label bias:** Annotations reflect human prejudices
- **Measurement bias:** Features are measured inconsistently across groups
- **Historical bias:** Data reflects past discrimination

### Model Hallucination
The model generates confident but incorrect outputs. Common in generative models (LLMs, diffusion models) but also occurs in traditional ML when:
- The model extrapolates beyond training data distribution
- Features are noisy or correlated with spurious patterns

### Representation Limitations
- Models are only as good as their training data
- Missing demographic groups lead to poor performance for those groups
- Correlation ≠ causation — models learn correlations, not causal relationships

---

## Notebooks

1. **[01-ml-fundamentals.ipynb](notebooks/01-ml-fundamentals.ipynb)** — Build and train models with scikit-learn
2. **[02-model-evaluation.ipynb](notebooks/02-model-evaluation.ipynb)** — Comprehensive metric evaluation
3. **[03-overfitting-underfitting.ipynb](notebooks/03-overfitting-underfitting.ipynb)** — Visualize and mitigate overfitting

## Exercises

- **[exercise-01.md](exercises/exercise-01.md)** — Practice building classifiers, evaluating models, and making business trade-offs

## Resources

- **[resources.md](resources.md)** — Links to documentation, tutorials, and datasets
