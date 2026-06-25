# 06 -- Async Python, Pydantic & Error Handling

> FastAPI runs on async Python. Without understanding these patterns, you'll write serving code with hard-to-find performance bugs.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ Python basics and functions
- ✅ FastAPI or async concepts
- ✅ Redis or caching basics
- ❓ Type hints in Python
- ❌ NOT required: Advanced async libraries

---

## Why Async Matters for ML Serving

```python
# SYNCHRONOUS: server blocks while waiting for Redis
def get_features(user_id):
    features = redis.get(user_id)     # blocks entire thread for 5ms
    # During this 5ms:
    #   - Request 2 arrives: must wait
    #   - Request 3 arrives: must wait
    #   - Request 4 arrives: must wait
    # Result: Queue builds up, latency increases exponentially
    return features                    

# At 1000 req/s, this creates a massive backlog
# 1000 requests × 5ms = 5 seconds of queuing!

# ASYNC: server handles other requests while waiting
async def get_features(user_id):
    features = await redis.get(user_id)  
    # Yields control while waiting
    # During this 5ms:
    #   - Request 2 processes: runs until it hits I/O
    #   - Request 3 processes: runs until it hits I/O
    #   - Request 4 processes: runs until it hits I/O
    # Result: All requests make progress simultaneously!
    return features

# With async:
# 4 requests running concurrently on 1 thread
# Appears as 4x throughput on single-core
```

**Impact in production:**
- Sync: 100 req/s max on single core
- Async: 400 req/s on same single core

---

## Core Async Patterns

```python
import asyncio

# Run multiple I/O operations concurrently (not sequentially)
async def get_all_features(user_id: str, merchant_id: str):
    # WRONG - Sequential: 5ms + 5ms + 5ms = 15ms
    # user_features = await redis.hgetall(f"user:{user_id}")
    # merchant_features = await redis.hgetall(f"merchant:{merchant_id}")
    # profile_features = await postgres.query(f"SELECT * FROM profiles WHERE id={user_id}")
    
    # RIGHT - Concurrent: max(5ms, 5ms, 5ms) = 5ms (3× faster)
    # asyncio.gather() starts all tasks simultaneously
    # asyncio.gather() waits for ALL to complete before returning
    user_features, merchant_features, profile_features = await asyncio.gather(
        redis.hgetall(f"user:{user_id}"),
        redis.hgetall(f"merchant:{merchant_id}"),
        postgres.query(f"SELECT * FROM profiles WHERE id={user_id}")
    )
    return user_features, merchant_features, profile_features

# Real production impact:
# Sequential: feature gathering takes 15ms
# Concurrent: feature gathering takes 5ms
# Model inference: 10ms
# Total sequential: 25ms
# Total concurrent: 15ms (40% faster end-to-end)
```

---

## Pydantic -- Input Validation

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class PredictionRequest(BaseModel):
    # Field() = define constraints on input
    user_id: str = Field(..., min_length=1, max_length=50)
    # ... = required, min_length/max_length = validate string length
    
    amount: float = Field(..., gt=0, lt=1_000_000,
                         description="Transaction amount in USD")
    # gt/lt = greater than / less than (must be 0 < amount < 1,000,000)
    
    merchant_category: str = Field(..., min_length=1)
    is_foreign: bool
    
    hour_of_day: int = Field(..., ge=0, le=23)
    # ge/le = greater/less than or equal
    
    credit_score: Optional[int] = Field(None, ge=300, le=850)
    # Optional = can be None, but if provided must be 300-850

    @validator("merchant_category")
    def must_be_valid_category(cls, v):
        # Custom validation: allowed values only
        valid = {"retail", "restaurant", "travel", "online", "atm", "other"}
        if v.lower() not in valid:
            raise ValueError(f"Invalid category '{v}'. Must be one of {valid}")
        return v.lower()  # normalize to lowercase

    class Config:
        extra = "forbid"    # reject unknown fields (prevents injection)

# FastAPI uses Pydantic automatically:
# Bad input (string in amount field) → 422 Unprocessable Entity (never reaches your code)
# Good input → typed Python object with guaranteed correct types

# Example bad requests:
# {"user_id": "", "amount": 100}  → REJECTED (empty user_id)
# {"user_id": "u1", "amount": -50}  → REJECTED (negative amount)
# {"user_id": "u1", "amount": "abc"}  → REJECTED (string not float)
# {"user_id": "u1", "amount": 100, "extra_field": "xyz"}  → REJECTED (extra field)
```

**Benefits:**
- Security: Rejects invalid data before your code touches it
- Type safety: No defensive None checks needed
- Documentation: Schema auto-generates API docs

---

## Error Handling and Graceful Degradation

```python
# Never let one request crash the server
@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        features = await get_features(request.user_id)
        prediction = float(model.predict_proba([features])[0, 1])
        return {"prediction": prediction, "source": "model"}

    except asyncio.TimeoutError:
        # Feature store too slow → use default features
        logger.warning(f"Feature timeout for user {request.user_id}")
        return {"prediction": DEFAULT_PREDICTION, "source": "timeout_fallback"}

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return {"prediction": DEFAULT_PREDICTION, "source": "error_fallback"}
```

---

## Caching Patterns

```python
import redis.asyncio as aioredis
import json, hashlib

redis_client = aioredis.Redis()

# Pattern 1: Feature caching (cache pre-computed features)
async def get_features_cached(user_id: str) -> dict:
    cache_key = f"features:user:{user_id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss: compute features (expensive)
    features = await compute_from_database(user_id)
    await redis_client.setex(cache_key, 300, json.dumps(features))  # 5 min TTL
    return features

# Pattern 2: Prediction caching (for repeated identical inputs)
async def predict_cached(request: PredictionRequest):
    cache_key = f"pred:{hashlib.md5(request.json().encode()).hexdigest()}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    result = await run_model(request)
    await redis_client.setex(cache_key, 3600, json.dumps(result))  # 1 hour TTL
    return result
```

---

## Secrets Management

```python
import os
from functools import lru_cache

# NEVER hardcode secrets
# DATABASE_URL = "postgresql://admin:password@prod:5432/ml"  ← WRONG

# RIGHT: read from environment
@lru_cache()
def get_settings():
    return {
        "database_url": os.environ["DATABASE_URL"],        # required
        "redis_url": os.environ["REDIS_URL"],              # required
        "model_version": os.environ.get("MODEL_VERSION", "Production"),  # optional with default
        "debug": os.environ.get("DEBUG", "false").lower() == "true"
    }

# In Kubernetes, inject from Secret:
# env:
#   - name: DATABASE_URL
#     valueFrom:
#       secretKeyRef:
#         name: ml-secrets
#         key: database_url
```

---

## Model Serialization Reference

| Model Type | Training Format | Production Serving | Security |
|---|---|---|---|
| sklearn | `.joblib` | ONNX Runtime | joblib: internal use only |
| XGBoost | `.ubj` (native) | ONNX Runtime | Safe |
| PyTorch | `.safetensors` (weights) | ONNX → TensorRT | SafeTensors: safe |
| HuggingFace | `.safetensors` | vLLM / TGI | SafeTensors: safe |
| Any | `.pkl` | Avoid in production | **UNSAFE** -- can execute arbitrary code |

```python
# SafeTensors: safe format for neural network weights
from safetensors.torch import save_file, load_file

save_file(model.state_dict(), "model.safetensors")
weights = load_file("model.safetensors")
model.load_state_dict(weights)
```

---

**Previous:** [05 -- SQL for MLOps](05-sql-for-mlops.md) | **Next:** [Career -- Interview Guide →](../career/01-interview-guide.md)
