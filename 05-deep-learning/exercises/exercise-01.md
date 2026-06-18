# Exercise 01: Deep Learning Practice

## Part 1: Build and Train a Simple Neural Network

### Task

Build a neural network in PyTorch that classifies handwritten digits (MNIST-style data).

### Requirements

1. **Create the dataset**: Use `torchvision.datasets.MNIST` or generate synthetic data with `sklearn.datasets.make_classification`
2. **Build the network**:
   - Input layer: 784 features (28×28 images flattened)
   - Hidden layer 1: 256 neurons, ReLU activation
   - Hidden layer 2: 128 neurons, ReLU activation
   - Output layer: 10 neurons (one per digit class)
3. **Train the model**:
   - Use CrossEntropyLoss
   - Use Adam optimizer with lr=0.001
   - Train for at least 5 epochs
   - Print training loss per epoch
4. **Evaluate**: Compute accuracy on test set

### Starter Code

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Define your model
class DigitClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        # TODO: Define layers
        pass

    def forward(self, x):
        # TODO: Forward pass
        pass

# Create model, loss, optimizer
model = DigitClassifier()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(5):
    # TODO: Training code
    pass
```

### Expected Output

- Training loss should decrease each epoch
- Final accuracy should be >90% on MNIST

---

## Part 2: Text Embeddings and Similarity

### Task

Generate embeddings for sentences and compute semantic similarity.

### Requirements

1. **Generate embeddings** for these sentences using a Hugging Face model:
   ```python
   sentences = [
       "The cat sat on the mat",
       "A feline rested on the rug",
       "The stock market crashed today",
       "Python is a programming language",
       "Dogs are loyal companions"
   ]
   ```

2. **Compute cosine similarity** between all pairs of sentences

3. **Answer**:
   - Which sentences are most similar?
   - Does the model capture semantic meaning?
   - Compare "The cat sat on the mat" vs "A feline rested on the rug" — what similarity score do you get?

4. **Visualize** the embeddings using PCA or t-SNE (reduce to 2D and plot)

### Starter Code

```python
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embedding(text):
    # Tokenize
    # Get model output
    # Mean pool over tokens
    # Return normalized embedding
    pass

# Compute embeddings and similarities
sentences = [...]
embeddings = [get_embedding(s) for s in sentences]
# TODO: Compute cosine similarity matrix
```

---

## Part 3: Compare Pre-trained Models

### Task

Use different pre-trained models on the same text and compare outputs.

### Requirements

1. **Use these pipelines**:
   ```python
   from transformers import pipeline

   sentiment = pipeline("sentiment-analysis")
   ner = pipeline("ner", aggregation_strategy="simple")
   summarization = pipeline("summarization")
   ```

2. **Test on these inputs**:
   - Sentiment: "I absolutely loved this movie, it was fantastic!"
   - NER: "Elon Musk founded SpaceX in Hawthorne, California in 2002."
   - Summarization: A 3-paragraph article about AI

3. **Document**:
   - Model names used (each pipeline defaults to a different model)
   - Output format for each task
   - Any surprising or interesting results

---

## Bonus: Fine-Tune a Small Model

### Task

Fine-tune a small pre-trained model on custom labeled data.

### Requirements

1. **Create a small dataset** (20-50 examples) of labeled text for binary classification (e.g., spam detection, sentiment)

2. **Load a pre-trained model**:
   ```python
   from transformers import AutoModelForSequenceClassification, AutoTokenizer

   model_name = "distilbert-base-uncased"
   model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
   tokenizer = AutoTokenizer.from_pretrained(model_name)
   ```

3. **Fine-tune** using the Hugging Face `Trainer` API

4. **Evaluate** accuracy on held-out examples

### Starter Code

```python
from transformers import TrainingArguments, Trainer

# Prepare dataset
train_texts = ["example 1", "example 2", ...]
train_labels = [0, 1, ...]

# Tokenize
train_encodings = tokenizer(train_texts, truncation=True, padding=True)

# Create dataset class
class SpamDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels)

# Train
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    learning_rate=2e-5,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)
trainer.train()
```

---

## Submission Checklist

- [ ] Part 1: Working neural network with training loop and >90% accuracy
- [ ] Part 2: Embeddings computed, similarity matrix, visualization
- [ ] Part 3: Three different models tested with documented outputs
- [ ] Bonus: Fine-tuned model with custom data
