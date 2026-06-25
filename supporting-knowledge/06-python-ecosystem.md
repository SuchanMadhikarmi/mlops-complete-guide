# 06 — Python ML Ecosystem


## Prerequisites

**Python basics:** Comfortable writing Python. Know what a package/library is. Can read documentation and stack traces.

**ML context:** Have trained at least one model. Understand training vs inference, batching, hardware acceleration basics.

**Required tools:** Python 3.8+ · pip · Jupyter notebooks helpful but not required

> The libraries you'll use every day. Focus on understanding what each does and when to use it — not memorizing APIs.
> The libraries you'll use every day. Focus on understanding what each does and when to use it — not memorizing APIs.

---

## NumPy — Foundation of Everything

All ML ultimately runs on numbers. NumPy is how Python handles them efficiently.

```python
import numpy as np

# Arrays are the building block
arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

# Vectorized operations (no Python loops needed)
arr * 2              # [2, 4, 6, 8, 10]
arr ** 2             # [1, 4, 9, 16, 25]
np.log(arr)          # [0, 0.69, 1.10, 1.39, 1.61]
arr.mean()           # 3.0
arr.std()            # 1.41

# 2D arrays (matrices = model weights)
matrix = np.array([[1, 2, 3], [4, 5, 6]])
matrix.shape         # (2, 3)
matrix.T             # transpose: (3, 2)
matrix @ matrix.T    # matrix multiplication: (2, 2)

# Common MLOps operations
np.isnan(predictions).any()    # check for NaN outputs
np.isinf(predictions).any()    # check for Inf outputs
np.clip(predictions, 0, 1)     # clamp probabilities to [0, 1]
```

**Why MLOps engineers need this:** Model inputs/outputs are NumPy arrays. Understanding shapes prevents the most common serving bugs (wrong dimensions, wrong dtypes).

---

## Pandas — Working With Data Tables

```python
import pandas as pd

# Load and inspect
df = pd.read_parquet("transactions.parquet")
df.shape          # (1000000, 15)
df.dtypes         # types of each column
df.describe()     # count, mean, std, min, percentiles, max
df.isnull().sum() # null counts per column

# Essential operations for MLOps
# ① Filter
fraud_only = df[df["is_fraud"] == 1]
recent = df[df["timestamp"] >= "2024-01-01"]

# ② Create features
df["amount_log"] = np.log1p(df["amount"])
df["hour"] = pd.to_datetime(df["timestamp"], utc=True).dt.hour

# ③ Aggregate (feature engineering)
user_features = df.groupby("user_id").agg(
    txn_count=("transaction_id", "count"),
    avg_amount=("amount", "mean"),
    fraud_count=("is_fraud", "sum")
).reset_index()

# ④ Join tables
full_df = transactions.merge(user_profiles, on="user_id", how="left")

# Common pitfall: SettingWithCopyWarning
df_filtered = df[df["age"] > 25]
df_filtered["new_col"] = 42  # WARNING — may not work

# Fix: use .copy()
df_filtered = df[df["age"] > 25].copy()
df_filtered["new_col"] = 42  # works correctly
```

### Polars — The Pandas Replacement (5–50x Faster)

```python
import polars as pl

# Polars syntax is similar but lazily evaluated (more efficient)
result = (
    pl.scan_parquet("transactions.parquet")  # lazy loading
    .filter(pl.col("amount") > 0)
    .groupby("user_id")
    .agg([
        pl.col("amount").mean().alias("avg_amount"),
        pl.col("transaction_id").count().alias("txn_count")
    ])
    .collect()  # execute
)
# Much faster than pandas for large datasets
```

---

## Scikit-learn — The ML Toolkit

```python
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, classification_report

# The consistent interface: all models work the same way
model = GradientBoostingClassifier(n_estimators=300, max_depth=5)
model.fit(X_train, y_train)              # train
predictions = model.predict(X_test)      # classify
probabilities = model.predict_proba(X_test)[:, 1]  # probability

# Pipeline: preprocessing + model bundled together
# Critical for production: preprocessing is part of the model
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", GradientBoostingClassifier(n_estimators=300))
])

pipeline.fit(X_train, y_train)      # fits imputer + scaler + model
pipeline.predict(X_test)             # applies same preprocessing automatically

# Save pipeline (includes all preprocessing params)
import joblib
joblib.dump(pipeline, "artifacts/fraud_pipeline.joblib")

# Load for serving
pipeline = joblib.load("artifacts/fraud_pipeline.joblib")
```

---

## PyTorch — Deep Learning

```python
import torch
import torch.nn as nn

# Define model
class FraudDetector(nn.Module):
    def __init__(self, input_dim: int):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.3),        # regularization
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1),
            nn.Sigmoid()            # output probability [0, 1]
        )
    
    def forward(self, x):
        return self.network(x)

model = FraudDetector(input_dim=20)

# Training
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.BCELoss()

for epoch in range(100):
    model.train()                   # enables dropout
    
    pred = model(X_train_tensor)
    loss = loss_fn(pred, y_train_tensor)
    
    optimizer.zero_grad()           # clear gradients
    loss.backward()                 # compute gradients
    optimizer.step()                # update weights

# INFERENCE — Critical production pattern
model.eval()                        # MUST call this — disables dropout
with torch.no_grad():               # saves memory and time
    probabilities = model(X_test_tensor)
    probabilities = probabilities.cpu().numpy()  # back to numpy for serving
```

---

## Hugging Face Transformers

```python
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# High-level: just works out of the box
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
result = classifier("This transaction looks suspicious")
# [{'label': 'NEGATIVE', 'score': 0.9998}]

# Lower-level: more control
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")

# Tokenize
inputs = tokenizer(
    "Sample text to classify",
    return_tensors="pt",
    truncation=True,
    max_length=512,
    padding=True
)

# Inference
model.eval()
with torch.no_grad():
    outputs = model(**inputs)
    probabilities = torch.softmax(outputs.logits, dim=-1)

# Serving considerations:
# - Models are large (250MB to 14GB+)
# - Use ONNX export for faster inference
# - Always use model.eval() and torch.no_grad()
# - Tokenizer must match the model exactly
```

---

## Key Library Versions (Pin These)

```txt
# requirements.txt — always pin exact versions for reproducibility
numpy==1.26.4
pandas==2.2.0
scikit-learn==1.4.0
torch==2.2.0
transformers==4.38.0
mlflow==2.10.0
fastapi==0.109.0
pydantic==2.5.3
evidently==0.4.16
feast==0.36.0
```

---

**Next:** [Practical Skills — Docker for ML →](../practical-skills/01-docker-for-ml.md)
