# 01 — Feature Stores (Feast + Redis)

> A Feature Store is the single infrastructure piece that most prevents training-serving skew. One feature definition, used in both training and serving.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ Redis basics (key-value store, caching)
- ✅ SQL and aggregations (GROUP BY, window functions)
- ✅ What training-serving skew is (read `02-continuous-training.md` first)
- ❓ Python Pandas and dataframes
- ❌ NOT required: Feast or Feast CLI experience

---

## The Training-Serving Skew Problem

This is where feature stores excel. They guarantee identical feature computation.

---

## Architecture: Feast + Redis + PostgreSQL

```
Raw Data (Database, Kafka)
         ↓
Feature Transformation Code (Python)
         ↓ (via feast materialize)
┌────────────────────────────────────┐
│         FEAST REGISTRY             │
│  (feature definitions + lineage)   │
├──────────────────┬─────────────────┤
│   Offline Store  │   Online Store  │
│   (PostgreSQL/   │   (Redis)       │
│    Parquet)      │                 │
│   Historical     │   Latest values │
│   Training data  │   <5ms serving  │
└──────────────────┴─────────────────┘
         ↑                    ↑
    Training Job          Serving API
    (batch reads)         (real-time reads)
```

---

## Feast Implementation

### Install and Configure

```bash
pip install feast[redis,postgres]

feast init fraud-feature-store
cd fraud-feature-store
```

```yaml
# feature_store.yaml
project: fraud_detection
registry: data/registry.db
provider: local
online_store:
  type: redis
  connection_string: "redis://localhost:6379"
offline_store:
  type: file  # or postgres for production
entity_key_serialization_version: 2
```

### Define Features

```python
# features/user_features.py
from datetime import timedelta
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from feast.types import Float32, Int64, Bool

# Entity: the "key" for features (what you're predicting about)
user = Entity(
    name="user_id",
    value_type=ValueType.STRING,
    description="Unique user identifier"
)

# Source: where the raw feature data comes from
user_stats_source = FileSource(
    path="data/user_stats.parquet",  # or BigQuery, Redshift, etc.
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp"
)

# FeatureView: group of related features with the same source and TTL
user_transaction_features = FeatureView(
    name="user_transaction_stats",
    entities=["user_id"],
    ttl=timedelta(days=1),  # how long online store values are valid
    schema=[
        Feature(name="avg_transaction_30d", dtype=Float32),
        Feature(name="transaction_count_30d", dtype=Int64),
        Feature(name="max_transaction_30d", dtype=Float32),
        Feature(name="fraud_count_90d", dtype=Int64),
        Feature(name="foreign_txn_rate_30d", dtype=Float32),
    ],
    source=user_stats_source,
    tags={"team": "risk", "owner": "ml-platform"},
)
```

### Materialize to Online Store

```bash
# Push features to Redis (online store) for serving
feast materialize-incremental $(date +%Y-%m-%dT%H:%M:%S)

# This reads from offline store and writes latest values to Redis
# Run this on a schedule (Airflow DAG, Kubernetes CronJob)
```

### Training: Point-in-Time Correct Feature Retrieval

```python
from feast import FeatureStore
import pandas as pd

store = FeatureStore(repo_path=".")

# Training data: user IDs with their event timestamps
# Point-in-time correctness: get features as they were AT THAT MOMENT
# Prevents using future information in training
entity_df = pd.DataFrame({
    "user_id": ["user_001", "user_002", "user_003"],
    "event_timestamp": pd.to_datetime([
        "2024-01-15 14:30:00",
        "2024-01-15 16:45:00",
        "2024-01-16 09:20:00"
    ], utc=True),
    "is_fraud": [0, 1, 0]  # label
})

# Feast retrieves feature values as they existed at each event_timestamp
# NOT the current values — prevents future data leakage
training_data = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "user_transaction_stats:avg_transaction_30d",
        "user_transaction_stats:transaction_count_30d",
        "user_transaction_stats:fraud_count_90d",
    ]
).to_df()

print(training_data.head())
# user_id | event_timestamp | is_fraud | avg_transaction_30d | ...
```

### Serving: Real-Time Feature Retrieval

```python
from feast import FeatureStore
import time

store = FeatureStore(repo_path=".")

async def get_features_for_prediction(user_id: str) -> dict:
    """Retrieve latest features from Redis — sub-millisecond"""
    start = time.time()
    
    features = store.get_online_features(
        features=[
            "user_transaction_stats:avg_transaction_30d",
            "user_transaction_stats:transaction_count_30d",
            "user_transaction_stats:fraud_count_90d",
            "user_transaction_stats:foreign_txn_rate_30d",
        ],
        entity_rows=[{"user_id": user_id}]
    ).to_dict()
    
    latency_ms = (time.time() - start) * 1000
    print(f"Feature retrieval: {latency_ms:.1f}ms")
    
    return {k: v[0] for k, v in features.items()}

# In serving API:
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Fetch precomputed features from Redis (fast)
    user_features = await get_features_for_prediction(request.user_id)
    
    # Combine with real-time request features
    all_features = {
        **user_features,
        "current_amount": request.amount,
        "is_foreign": request.is_foreign,
        "hour_utc": request.hour_utc
    }
    
    return model.predict(all_features)
```

---

## Point-in-Time Correctness — Why It Matters

```
Scenario: Predict loan default using credit score history

WRONG (without point-in-time):
  Loan event: Jan 15, 2024
  User's CURRENT credit score (Dec 2024): 720
  → Model trains on Dec 2024 data to predict Jan 2024 event
  → Uses information from the FUTURE
  → Model learns patterns that didn't exist yet
  → Production: completely wrong predictions

RIGHT (with point-in-time via Feast):
  Loan event: Jan 15, 2024
  Credit score AS OF Jan 15, 2024: 650
  → Model trains on exactly what was known at prediction time
  → Realistic evaluation → reliable production performance
```

---

## Materialization Schedule (Airflow DAG)

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

dag = DAG(
    "feature_store_materialization",
    schedule_interval="0 * * * *",  # Every hour
    start_date=datetime(2024, 1, 1),
    catchup=False
)

materialize = BashOperator(
    task_id="materialize_features",
    bash_command="""
        cd /opt/feast/fraud-feature-store
        feast materialize-incremental $(date -u +%Y-%m-%dT%H:%M:%S)
    """,
    dag=dag
)
```

---

**Next:** [02 — Continuous Training →](02-continuous-training.md)
