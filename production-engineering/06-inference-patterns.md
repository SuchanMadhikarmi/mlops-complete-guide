# 06 -- Batch vs Real-Time Inference Patterns

## Prerequisites

**ML/Serving knowledge:** Have deployed at least one model endpoint. Understand what prediction latency means and why it matters.

**Infrastructure perspective:** Know the difference between scheduled jobs and always-on services. Familiar with concept of "at-rest" vs "reactive" systems.

**Required understanding:** Trade-offs between freshness, cost, and complexity. When to use which pattern based on requirements.

> Choosing the wrong inference pattern makes your system either too slow, too expensive, or both.

## Why This Matters (The Business Perspective)

Every company asks: "How do we serve predictions?" The answer affects:
- **Cost:** Batch = cheap. Real-time = expensive. Streaming = medium.
- **User experience:** Real-time = instant. Batch = delayed.
- **Engineering complexity:** Batch = simple. Real-time = complex. Streaming = medium.

You must match the pattern to the requirement, not the other way around.

---

## Batch Inference -- Predict Everything in Advance

Run predictions on a large dataset on a schedule. Store results. Applications read pre-computed results.

```python
# Airflow DAG: nightly batch scoring
@task
def batch_score_all_users():
    # Load all active users
    users = pd.read_parquet("s3://data/active_users.parquet")

    # Load production model
    model = mlflow.sklearn.load_model("models:/churn_predictor/Production")

    # Batch predict (much faster than one-at-a-time)
    probabilities = model.predict_proba(users[FEATURE_COLS])[:, 1]

    # Store results for application to read
    results = users[["user_id"]].copy()
    results["churn_probability"] = probabilities
    results["scored_at"] = pd.Timestamp.utcnow()
    results.to_parquet("s3://predictions/churn_scores_latest.parquet")
    results.to_sql("churn_scores", db_connection, if_exists="replace")

# Application reads from DB (sub-millisecond)
# Model doesn't need to be running 24/7
```

**Use when:** Predictions don't need to be instant. Email campaigns, daily credit reviews, weekly recommendations.

**Advantages:**
- Cheap: GPU only runs 1-2 hours/day
- Simple: no serving infrastructure
- Can use powerful hardware efficiently (full GPU utilization)

**Disadvantages:** Predictions are stale -- can't react to what user did in the last 5 minutes.

**Production consequence:** A churn prediction model built with batch inference at a B2C company saved $100k/year in compute costs compared to real-time inference.

---

## Real-Time Inference -- Predict On Demand

Model runs on-demand, within milliseconds, in response to each request.

```python
# FastAPI serving -- always running, always ready
@app.post("/predict")
async def predict(request: PredictionRequest):
    start = time.time()

    # Fetch precomputed features from Redis (fast)
    user_features = await redis.hgetall(f"user:{request.user_id}")

    # Combine with real-time request features
    features = {
        **user_features,
        "current_amount": request.amount,
        "is_foreign": request.is_foreign,
        "hour_utc": datetime.utcnow().hour
    }

    # Predict
    probability = model.predict_proba([list(features.values())])[0, 1]

    latency_ms = (time.time() - start) * 1000
    return {"fraud_probability": float(probability), "latency_ms": latency_ms}
```

**Use when:** Decision must happen in real-time. Fraud detection, search ranking, dynamic pricing.

**Advantages:**
- Fresh predictions: always reflects current context
- Highly personalized: incorporates real-time request data
- Reacts immediately to changes

**Disadvantages:**
- Expensive: model runs 24/7
- Latency pressure: every ms counts
- Complex infrastructure: need caching, monitoring, failover

**Production consequence:** Real-time fraud detection catches fraud immediately. Batch detection (once/day) misses intra-day fraud patterns.

---

## Streaming Inference -- Near Real-Time

Process predictions as events stream in. Not waiting for batch, not fully synchronous.

```python
from confluent_kafka import Consumer, Producer
import json

consumer = Consumer({"bootstrap.servers": "kafka:9092", "group.id": "fraud-scorer"})
producer = Producer({"bootstrap.servers": "kafka:9092"})
consumer.subscribe(["raw-transactions"])

model = load_model()

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        continue

    transaction = json.loads(msg.value())
    features = prepare_features(transaction)
    fraud_score = float(model.predict_proba([features])[0, 1])

    # Produce result to downstream topic
    result = {**transaction, "fraud_score": fraud_score, "scored_at": time.time()}
    producer.produce("scored-transactions", json.dumps(result).encode())
    producer.poll(0)
```

**Use when:** You need freshness (seconds, not hours) but can tolerate a few seconds of latency. Post-transaction fraud review (doesn't block transaction but flags within seconds).

**Advantages:**
- Fresh: seconds old, not hours
- Cheaper than real-time: can batch internally
- Less complexity than real-time: no synchronous latency pressure

**Disadvantages:**
- Not instant: 2-5 seconds latency typical
- Streaming infrastructure overhead (Kafka, schemas, monitoring)

---

## The Hybrid Pattern (Production Reality)

Most mature ML systems combine all three:

```
Batch layer (runs nightly):
  → user's 30-day transaction statistics → stored in Redis
  → merchant's historical fraud rate     → stored in Redis
  → user's risk tier classification      → stored in database

Real-time layer (at prediction time):
  → current transaction amount
  → current device fingerprint
  → current time/location

Serving API joins both at prediction time:
  fetch batch features from Redis (2ms)
  + compute real-time features from request (0ms)
  → model inference (10ms)
  → total: ~15ms end-to-end
```

**Why hybrid?** Batch features (slow-changing) are precomputed. Real-time features (fast-changing) are computed on-demand. Results in low latency + low cost.

---

## Decision Framework

```
Latency requirement?
├── < 100ms (blocking user action)     → Real-time inference
├── Seconds OK (async notification)    → Streaming inference
└── Hours OK (daily campaign)          → Batch inference

Data freshness requirement?
├── Must reflect last 5 minutes        → Real-time
├── Last few minutes OK                → Streaming
└── Yesterday's data OK                → Batch

Cost sensitivity?
├── High (minimize infrastructure)     → Batch
├── Medium                             → Streaming
└── Low (performance over cost)        → Real-time
```

---

**Previous:** [05 -- Model Explainability](05-model-explainability.md) | **Next:** [Advanced -- Distributed Training →](../advanced-specialized/01-distributed-training.md)
