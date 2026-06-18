# Module 03: Data Engineering for AI

> Peserta akan memahami berbagai jenis data dalam sistem AI, sumber data, teknik pembersihan dan transformasi data, serta membangun pipeline data sederhana.

## Learning Objectives

By the end of this module, you will be able to:

- Identify types of data used in AI systems: structured, text, image, audio
- Locate and load datasets from Kaggle, Hugging Face Datasets, and public APIs
- Diagnose common data problems: missing values, duplicates, inconsistent formats
- Clean data using Pandas: handling nulls, fixing types, string cleanup
- Transform data: normalization, standardization, one-hot encoding, label encoding
- Process text data: lowercasing, tokenization, stopword removal
- Engineer basic features from existing data
- Build a simple end-to-end data pipeline: fetch → clean → transform → save

---

## 1. Types of Data in AI Systems

AI systems consume different kinds of data, each requiring different preprocessing:

### Structured Data
Tabular data with fixed columns and rows. Stored in CSV, SQL databases, or spreadsheets.

| Format | Example | Tools |
|--------|---------|-------|
| CSV | Customer transactions | Pandas, SQL |
| JSON | API responses | Pandas `read_json`, `json` module |
| Database tables | User records | SQLAlchemy, pandas `read_sql` |
| Excel | Sales reports | `openpyxl`, `read_excel` |

### Text Data
Unstructured sequences of characters. Used in NLP, chatbots, RAG systems.

- Documents, emails, chat logs, reviews, code
- Preprocessing: tokenization, lowercasing, stopword removal, stemming/lemmatization
- Representation: TF-IDF, word embeddings, transformer tokenization

### Image Data
Grids of pixel values. Used in computer vision, multimodal AI.

- Photos, medical scans, screenshots, diagrams
- Preprocessing: resizing, normalization (pixel values 0-1), augmentation
- Representation: pixel arrays (numpy), feature maps (CNNs)

### Audio Data
Time-series of amplitude values. Used in speech recognition, voice assistants.

- Voice recordings, music, environmental sounds
- Preprocessing: resampling, spectrogram conversion, silence removal
- Representation: waveform arrays, MFCC features, spectrograms

```
AI Data Taxonomy
├── Structured
│   ├── Tabular (CSV, SQL)
│   └── Time-series (logs, sensor data)
└── Unstructured
    ├── Text (documents, chat)
    ├── Image (photos, scans)
    └── Audio (speech, music)
```

---

## 2. Data Sources

### Public Datasets
Pre-collected datasets for research and learning.

| Source | Content | Access |
|--------|---------|--------|
| [Kaggle Datasets](https://www.kaggle.com/datasets) | 200k+ datasets across domains | Free account, some need GPU |
| [Hugging Face Datasets](https://huggingface.co/datasets) | NLP, CV, multimodal datasets | `pip install datasets` |
| [UCI ML Repository](https://archive.ics.uci.edu/ml) | Classic ML datasets | Direct download |
| [Google Dataset Search](https://datasetsearch.research.google.com/) | Meta-search for datasets | Web |
| [Papers With Code](https://paperswithcode.com/datasets) | Datasets linked to research papers | Web |

### APIs
Programmatic access to live data.

```python
# Example: Fetching data from a public API
import requests

response = requests.get("https://api.github.com/repos/python/cpython/issues")
issues = response.json()
```

### Internal Company Data
Production data from databases, logs, and business systems. Requires access permissions and often significant cleaning.

---

## 3. Exploring Datasets from Kaggle and Hugging Face

### Kaggle

```python
# Install: pip install kaggle
# Set up ~/.kaggle/kaggle.json with your API token

import kaggle

# Search for datasets
kaggle.api.dataset_list(search="titanic")

# Download a dataset
kaggle.api.dataset_download_files(
    dataset="titanic/titanic",
    path="./data",
    unzip=True
)
```

### Hugging Face Datasets

```python
# Install: pip install datasets

from datasets import load_dataset

# Load a dataset
dataset = load_dataset("imdb")

# Explore structure
print(dataset)
print(dataset["train"][0])

# Convert to Pandas
df = dataset["train"].to_pandas()
df.head()
```

---

## 4. Common Dataset Problems

Real-world data is messy. Here are the most frequent issues:

### Missing Values
Cells with no data. Appear as `NaN`, `None`, `""`, `"N/A"`, or `-`.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name": ["Alice", "Bob", None, "Dave"],
    "age": [25, np.nan, 30, 28],
    "email": ["a@mail.com", "b@mail.com", "c@mail.com", ""]
})

print(df.isnull().sum())
# name    1
# age     1
# email   0
```

### Duplicates
Identical or near-identical rows that skew analysis.

```python
df.duplicated().sum()  # Count duplicates
df.drop_duplicates(inplace=True)  # Remove them
```

### Inconsistent Formats
Same data represented differently.

| Problem | Example | Fix |
|---------|---------|-----|
| Date formats | "2024-01-15", "15/01/2024", "Jan 15" | Standardize to datetime |
| Capitalization | "New York", "new york", "NEW YORK" | Lowercase or title case |
| Units | "5kg", "5 kg", "5000g" | Standardize units |
| Categories | "male", "Male", "M", "m" | Map to single value |

### Outliers
Extreme values that don't represent the true distribution.

```python
# Detect with IQR
Q1 = df["age"].quantile(0.25)
Q3 = df["age"].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df["age"] < Q1 - 1.5*IQR) | (df["age"] > Q3 + 1.5*IQR)]
```

---

## 5. Data Cleaning with Pandas

### Handling Missing Values

```python
# Drop rows with any null
df.dropna(inplace=True)

# Drop rows where specific columns are null
df.dropna(subset=["name", "age"], inplace=True)

# Fill with constant
df["age"].fillna(0, inplace=True)

# Fill with mean/median/mode
df["age"].fillna(df["age"].mean(), inplace=True)

# Forward/backward fill (for time series)
df["value"].fillna(method="ffill", inplace=True)

# Interpolation
df["value"].interpolate(inplace=True)
```

### Removing Duplicates

```python
# Exact duplicates
df.drop_duplicates(inplace=True)

# Duplicates based on specific columns
df.drop_duplicates(subset=["name", "email"], inplace=True)

# Keep last occurrence instead of first
df.drop_duplicates(keep="last", inplace=True)
```

### Fixing Data Types

```python
# Convert to datetime
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

# Convert to numeric
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Convert to categorical
df["category"] = df["category"].astype("category")
```

### String Cleaning

```python
# Strip whitespace
df["name"] = df["name"].str.strip()

# Lowercase
df["email"] = df["email"].str.lower()

# Replace values
df["phone"] = df["phone"].str.replace("-", "")

# Extract patterns
df["domain"] = df["email"].str.extract(r"@(.+)")
```

---

## 6. Data Transformation

### Normalization (Min-Max Scaling)
Scales values to range [0, 1]. Good for algorithms sensitive to magnitude.

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
df[["age", "salary"]] = scaler.fit_transform(df[["age", "salary"]])
```

### Standardization (Z-score Scaling)
Centers data around mean=0, std=1. Good for algorithms assuming normal distribution.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df[["age", "salary"]] = scaler.fit_transform(df[["age", "salary"]])
```

### One-Hot Encoding
Converts categorical variables to binary columns. Use when categories have no ordinal relationship.

```python
pd.get_dummies(df, columns=["color"], prefix="color")
# color_blue  color_green  color_red
# 1           0            0
# 0           1            0
```

### Label Encoding
Assigns integer to each category. Use for ordinal data (low < medium < high).

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df["size_encoded"] = le.fit_transform(df["size"])
# S=0, M=1, L=2
```

---

## 7. Text Data Processing Basics

```python
import re

# Lowercase
text = text.lower()

# Tokenize (split into words)
tokens = text.split()

# Remove punctuation
tokens = [re.sub(r"[^\w\s]", "", token) for token in tokens]

# Remove stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
tokens = [t for t in tokens if t not in stop_words and t]

# Stemming / Lemmatization
from nltk.stem import PorterStemmer, WordNetLemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

stemmed = [stemmer.stem(t) for t in tokens]
lemmatized = [lemmatizer.lemmatize(t) for t in tokens]
```

---

## 8. Feature Engineering Fundamentals

Creating new features from existing data to improve model performance.

### From Numeric Data
```python
# Binning
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 35, 60, 100],
                          labels=["child", "young_adult", "adult", "senior"])

# Ratios
df["debt_to_income"] = df["debt"] / df["income"]

# Log transform (for skewed distributions)
df["log_income"] = np.log1p(df["income"])
```

### From Text Data
```python
# Text length
df["review_length"] = df["review"].str.len()

# Word count
df["word_count"] = df["review"].str.split().str.len()

# Contains keyword
df["has_negative"] = df["review"].str.contains("bad|terrible|awful", case=False)
```

### From Date/Time
```python
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day_of_week"] = df["date"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
```

---

## 9. Building a Simple Data Pipeline

A data pipeline automates the flow: **Fetch → Clean → Transform → Save**.

```
┌──────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────┐
│  FETCH   │ ──► │  CLEAN   │ ──► │  TRANSFORM  │ ──► │   SAVE   │
│          │     │          │     │             │     │          │
│ API call │     │ Handle   │     │ Normalize   │     │ CSV file │
│ CSV load │     │ nulls    │     │ Encode      │     │ Database │
│ Web scrape│    │ Duplicates│    │ Features    │     │ GitHub   │
└──────────┘     └──────────┘     └─────────────┘ └──────────┘
```

### Pipeline Structure

```python
import pandas as pd

def fetch_data(filepath):
    """Load raw data."""
    return pd.read_csv(filepath)

def clean_data(df):
    """Handle missing values, duplicates, types."""
    df = df.drop_duplicates()
    df = df.dropna(subset=["critical_column"])
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df

def transform_data(df):
    """Normalize, encode, feature engineering."""
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    df[["age", "salary"]] = scaler.fit_transform(df[["age", "salary"]])
    df = pd.get_dummies(df, columns=["category"])
    return df

def save_data(df, output_path):
    """Save cleaned data."""
    df.to_csv(output_path, index=False)

# Run pipeline
raw = fetch_data("data/raw.csv")
cleaned = clean_data(raw)
transformed = transform_data(cleaned)
save_data(transformed, "data/cleaned.csv")
```

### Pushing to GitHub

```bash
git add data/cleaned.csv
git commit -m "feat: add cleaned dataset for module 03"
git push origin main
```

> **Note**: Large data files should use [Git LFS](https://git-lfs.com/) or be excluded via `.gitignore`.

---

## Notebooks

- [01 - Explore Datasets](notebooks/01-explore-datasets.ipynb)
- [02 - Data Cleaning](notebooks/02-data-cleaning.ipynb)
- [03 - Transformation & Encoding](notebooks/03-transformation-encoding.ipynb)
- [04 - Simple Pipeline](notebooks/04-simple-pipeline.ipynb)

## Exercises

- [Exercise 01: Data Engineering Practice](exercises/exercise-01.md)

## Resources

- [Resources & References](resources.md)
