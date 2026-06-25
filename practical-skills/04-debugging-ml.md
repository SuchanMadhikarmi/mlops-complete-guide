# 04 -- Debugging ML Systems

> ML debugging is different from software debugging because failures are often silent and statistical. Use a systematic approach.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ Kubernetes debugging basics (logs, exec, describe)
- ✅ Python debugging
- ✅ Basic system troubleshooting
- ❓ Model serving concepts (read `../core-mlops/03-model-serving.md`)
- ❌ NOT required: Advanced performance profiling

---

## The Key Difference: Silent Failures

Always work from infrastructure inward. Most issues are NOT in the model code.

```
Level 1: Infrastructure  → CPU/GPU/memory/network issues
Level 2: Data            → Bad input, pipeline failure, schema change
Level 3: Model           → Wrong version, degraded, serving bug
Level 4: Business logic  → Wrong threshold, postprocessing bug
```

---

## Common Scenarios and Root Causes

### "Predictions suddenly all cluster around 0.5"

```bash
# Model is suddenly uncertain about everything

# Check 1: Is model in training mode? (dropout active)
kubectl exec <pod> -- python -c "
import mlflow
model = mlflow.pytorch.load_model('...')
print('Is training mode:', model.training)   # should be False in serving
"
# Fix: model.eval() before serving

# Check 2: Are input features all zeros/nulls?
kubectl exec <pod> -- python -c "
import requests
resp = requests.post('http://localhost:8000/debug/features', json={'user_id': 'u123'})
print(resp.json())
"
# Fix: investigate feature pipeline (Redis connection? Feature materialization?)

# Check 3: Wrong model version loaded?
kubectl logs <pod> | grep "Loading model"
# Fix: verify MODEL_VERSION env var, check registry
```

### "Latency suddenly doubled"

```bash
# Step 1: Check pod resource usage
kubectl top pods --sort-by=cpu

# Step 2: Check if new model was deployed recently
kubectl rollout history deployment/fraud-serving

# Step 3: Isolate where latency is coming from
kubectl exec <pod> -- python -c "
import time, redis, numpy as np
from src.model import load_model

r = redis.Redis()
model = load_model()

# Test each component independently
for component, fn in [
    ('Redis lookup', lambda: r.hgetall('user:test123')),
    ('Model inference', lambda: model.predict_proba(np.random.rand(1,20))),
]:
    start = time.time()
    fn()
    print(f'{component}: {(time.time()-start)*1000:.1f}ms')
"
```

### "Training loss is NaN"

```python
# Debugging training NaN
def debug_nan_loss(model, X_batch, y_batch, optimizer, loss_fn):
    # Check 1: NaN in input data?
    if X_batch.isnan().any():
        print(f"NaN in input! Columns: {X_batch.isnan().any(dim=0)}")
        return

    # Check 2: Gradient exploding?
    loss = loss_fn(model(X_batch), y_batch)
    loss.backward()

    for name, param in model.named_parameters():
        if param.grad is not None:
            grad_norm = param.grad.norm()
            if grad_norm > 100:
                print(f"Exploding gradient in {name}: {grad_norm:.2f}")

    # Fix: gradient clipping
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
```

### "Works locally, fails in production"

```python
# Checklist for this classic problem:
checks = [
    "Python version matches? (local vs container)",
    "Library versions identical? (pin in requirements.txt)",
    "Environment variables all set? (MLFLOW_URI, REDIS_URL, etc.)",
    "GPU vs CPU difference? (some ops differ slightly)",
    "Feature pipeline accessible? (test Redis/feature store connection)",
    "Preprocessing same as training? (use sklearn Pipeline to avoid this)",
    "Model loaded correctly? (check logs for load confirmation)",
    "Enough memory? (large models need 2-4x their size for inference)",
]
for check in checks:
    print(f"[ ] {check}")
```

---

## Production Debugging Commands

```bash
# View logs from crashed container (before restart)
kubectl logs <pod> --previous --tail=200

# Shell into running container
kubectl exec -it <pod> -- /bin/bash

# Why is pod not scheduling?
kubectl describe pod <pod>   # read Events section at bottom

# GPU memory state
kubectl exec <pod> -- nvidia-smi

# Check environment variables
kubectl exec <pod> -- env | grep -E "MLFLOW|REDIS|MODEL"

# Port-forward for local testing
kubectl port-forward svc/fraud-serving 8000:8000
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
     -d '{"user_id":"test","amount":150.0,"is_foreign":false,"hour_of_day":14}'

# Test Redis feature store directly
kubectl exec <pod> -- python -c "
import redis
r = redis.Redis(host='redis-service', port=6379)
print(r.hgetall('user:test123'))
"
```

---

## Debugging Tips by Experience Level

| If you're debugging... | Start here |
|---|---|
| NaN loss | Check data quality first, then LR |
| High serving latency | Profile each component separately |
| Works locally, fails in prod | Compare env vars and library versions |
| Model accuracy dropped | Check if training data distribution changed |
| Predictions non-deterministic | `model.eval()` not called |
| OOM errors | Reduce batch size (training) or model/replica count (serving) |
| Pod stuck in Pending | `kubectl describe pod` → Events section |
| High null rate in features | Feature pipeline broken, check upstream |

---

**Next:** [05 -- SQL for MLOps →](05-sql-for-mlops.md)
