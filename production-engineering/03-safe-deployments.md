# 03 — Safe Deployments: Shadow, A/B Testing & Canary Rollouts

> Never deploy a new model directly to 100% of production traffic. The safe path is always: **Shadow → Canary → Production**. This guide explains each step and why skipping any of them is dangerous.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ Model versioning and champion-challenger pattern (read `02-continuous-training.md`)
- ✅ Kubernetes traffic routing or load balancer basics
- ✅ Basic statistics (p-values, significance)
- ❓ Monitoring and alerting concepts
- ❌ NOT required: Advanced A/B test methodology

---

## Why You Can't Just Deploy a New Model

This is different from software deployments. Test sets are historical. Production is live and changing.

- Future traffic patterns
- Edge cases that weren't in your test data
- System behavior under real load
- Latency under production conditions
- Business metric impact (which may differ from model accuracy)

You need a way to test on real production traffic without risking real users. That's exactly what shadow deployments and canary rollouts provide.

---

---

## When to Use Each Stage

### What It Is

Both models run on every request simultaneously. Only the **champion**'s prediction is served to the user. The **challenger**'s prediction is logged but silently discarded.

```
Incoming Request
       │
       ├──────────────────────────────────┐
       │                                  │
       ▼                                  ▼
Champion Model                    Challenger Model
(Production)                      (New Model)
       │                                  │
       │ prediction SERVED to user        │ prediction LOGGED only
       │                                  │ (never shown to user)
       ▼                                  ▼
   User Response               Monitoring / Log Store
```

### What You Learn from Shadow Mode

- Does the challenger produce different predictions? For which inputs?
- Is it slower? Does it use more memory?
- Does it crash on any edge cases not in your test set?
- Where do the two models disagree most? Which one is correct?

### How Long to Run Shadow Mode

| Traffic Volume | Minimum Duration |
|---|---|
| Low (< 1k req/day) | 72 hours |
| Medium (1k–10k req/day) | 48 hours |
| High (> 10k req/day) | 24 hours |

Run until you have statistically sufficient samples from both models on the same inputs.

### Implementation Pattern

```python
# model_router.py
import asyncio
import logging

logger = logging.getLogger(__name__)

async def serve_with_shadow(request, champion, challenger):
    """
    Serve champion prediction, run challenger in background.
    """
    # Run both models simultaneously (not sequentially)
    champion_pred, challenger_pred = await asyncio.gather(
        champion.predict_async(request),
        challenger.predict_async(request)
    )
    
    # Log challenger for analysis (never serve it)
    logger.info({
        "event": "shadow_prediction",
        "request_id": request.id,
        "champion_pred": float(champion_pred),
        "challenger_pred": float(challenger_pred),
        "champion_version": champion.version,
        "challenger_version": challenger.version,
        "inputs": request.features  # for debugging disagreements
    })
    
    # Only serve champion prediction
    return champion_pred
```

---

## Stage 2 — A/B Testing (Real Traffic Split)

### What It Is

Real users receive predictions from either the champion or the challenger. You split traffic and measure real business outcomes.

**Key difference from shadow mode:** In A/B testing, users actually see the challenger's predictions. This tells you something shadow mode cannot: does the new model produce better *business outcomes* (clicks, conversions, revenue)?

```
Incoming Requests
       │
       ▼
  Traffic Router
  (hash user_id)
       │
   ┌───┴───┐
   │       │
   ▼       ▼
  90%     10%
Champion  Challenger
  │         │
  │         │
  ▼         ▼
Business Metrics tracked separately per group
```

### The Non-Negotiable A/B Testing Rules

**1. Calculate sample size before starting**

```python
# How many samples do you need?
# Depends on:
# - Minimum detectable effect (how small an improvement do you care about?)
# - Significance level (α = 0.05 standard)
# - Statistical power (1 - β = 0.80 standard)

# Use Evan Miller's A/B calculator or scipy:
from scipy import stats

def calculate_sample_size(baseline_rate, min_effect, alpha=0.05, power=0.80):
    """
    baseline_rate: Current conversion/fraud rate
    min_effect: Minimum improvement you care about (e.g., 0.02 = 2%)
    """
    p1 = baseline_rate
    p2 = baseline_rate + min_effect
    
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    n = ((z_alpha + z_beta)**2 * (p1*(1-p1) + p2*(1-p2))) / (p2-p1)**2
    return int(n)

# Example: 1% baseline fraud rate, want to detect 0.2% improvement
n = calculate_sample_size(0.01, 0.002)
print(f"Need {n} samples per group")
```

**2. Ensure consistent assignment**

The same user must always see the same model during the test.

```python
import hashlib

def assign_model(user_id: str, challenger_percent: float = 10.0) -> str:
    """
    Consistently assign users to groups using hash.
    Same user_id always → same group (no flipping between requests).
    """
    hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    bucket = hash_value % 100  # 0-99
    
    if bucket < challenger_percent:
        return "challenger"
    return "champion"
```

**3. Define automatic stop conditions before starting**

```python
GUARDRAILS = {
    "max_error_rate": 0.05,      # stop if error rate > 5%
    "max_latency_p99_ms": 200,   # stop if P99 latency > 200ms
    "min_business_metric": 0.95  # stop if business metric drops > 5%
}

def check_guardrails(challenger_metrics: dict) -> bool:
    """Returns True if test should stop."""
    if challenger_metrics["error_rate"] > GUARDRAILS["max_error_rate"]:
        alert("A/B test stopped: challenger error rate too high")
        return True
    if challenger_metrics["latency_p99"] > GUARDRAILS["max_latency_p99_ms"]:
        alert("A/B test stopped: challenger too slow")
        return True
    return False
```

**4. Test one thing at a time**

If you change the model AND the UI AND run a marketing campaign simultaneously, you cannot attribute results to any single change.

---

## Stage 3 — Canary Rollout (Gradual Promotion)

### What It Is

Gradually shift traffic from champion to challenger in increasing increments. Monitor at each stage before proceeding.

```
Stage 1:   5% challenger  → Wait 30-60 min → Check: no errors, normal latency
Stage 2:  25% challenger  → Wait 2-4 hours → Check: business metrics on par
Stage 3:  50% challenger  → Wait 4-8 hours → Last easy rollback point
Stage 4: 100% challenger  → Challenger becomes new champion
```

### The Traffic Configuration (Hot-Reloadable)

```yaml
# model_routing_config.yaml
# This file is watched by the router — changes take effect immediately
# Rollback = edit this file, no code change needed

model_routing:
  champion:
    model_name: "fraud_detector"
    version: "v22"
    traffic_percent: 75
    
  canary:
    model_name: "fraud_detector" 
    version: "v23"
    traffic_percent: 25
    
  rollback_on_error_rate: 0.02   # auto-rollback if >2% errors
  rollback_on_latency_p99: 150   # auto-rollback if P99 > 150ms
```

```python
# model_router.py — reads config at runtime
import yaml
import time

class ModelRouter:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()
        self.last_loaded = time.time()
    
    def load_config(self):
        with open(self.config_path) as f:
            return yaml.safe_load(f)
    
    def route_request(self, request_id: str):
        # Reload config every 30 seconds (hot-reload)
        if time.time() - self.last_loaded > 30:
            self.config = self.load_config()
            self.last_loaded = time.time()
        
        champion_pct = self.config["model_routing"]["champion"]["traffic_percent"]
        
        # Consistent hash-based routing
        bucket = hash(request_id) % 100
        if bucket < champion_pct:
            return "champion"
        return "canary"
```

### Automatic Rollback

```python
from prometheus_client import Counter, Histogram
import yaml

error_counter = Counter('model_errors_total', 'Model errors', ['model_version'])
latency_histogram = Histogram('model_latency_ms', 'Latency', ['model_version'])

async def serve_with_canary(request):
    router = ModelRouter("config/routing.yaml")
    assigned_model = router.route_request(request.id)
    
    model = load_model(assigned_model)
    
    start = time.time()
    try:
        prediction = await model.predict(request)
        latency_ms = (time.time() - start) * 1000
        latency_histogram.labels(model_version=assigned_model).observe(latency_ms)
        
        # Check latency guardrail
        if latency_ms > 150 and assigned_model == "canary":
            trigger_rollback(reason=f"P99 latency {latency_ms}ms > 150ms threshold")
        
        return prediction
        
    except Exception as e:
        error_counter.labels(model_version=assigned_model).inc()
        
        # Check error rate (evaluated by Prometheus alert rules)
        # If canary error rate > 2%, alertmanager calls /rollback endpoint
        raise
```

---

## The Rollback Procedure

Rollback must be instant — under 30 seconds — and must not require code changes or redeployments.

```bash
# Rollback = edit config file
# Option 1: Direct edit
sed -i 's/traffic_percent: 25/traffic_percent: 0/' config/routing.yaml
sed -i 's/traffic_percent: 75/traffic_percent: 100/' config/routing.yaml

# Option 2: Replace with known-good config
cp config/routing_champion_only.yaml config/routing.yaml

# Option 3: GitOps — merge rollback PR (changes reflected in ~60 seconds)
git checkout -b rollback/fraud-model-v23
# edit routing.yaml
git commit -m "Rollback: fraud-model-v23 causing latency spike"
git push && gh pr merge --auto
```

---

## Decision Framework: Which Stage to Use

```
New model ready for testing
          │
          ▼
Is the model business-critical?
(fraud, medical, financial)
          │
    ┌─────┴─────┐
    │           │
   YES          NO
    │           │
    ▼           ▼
Shadow mode  Can skip shadow,
required     go straight to canary
    │
    ▼
Shadow mode passes?
(no errors, latency ok, reasonable predictions)
    │
    ▼
A/B test (if business metric measurement needed)
    OR
Canary rollout (if confident from shadow data)
    │
    ▼
Canary at 5% → 25% → 50% → 100%
Each stage must pass guardrail checks
```

---

## What to Monitor at Each Stage

### During Shadow Mode
- Does challenger crash on any inputs?
- Agreement rate between champion and challenger
- Latency of challenger (even though it's not served)
- Memory usage of challenger

### During A/B Testing
- Statistical significance of metric differences
- Business KPIs per group (not just model metrics)
- Error rates per group
- User experience metrics per group

### During Canary Rollout
- Error rate (target: < 1% difference from champion)
- Latency P50, P95, P99 (target: within 20% of champion)
- Prediction distribution (target: similar shape to champion)
- Business metrics (target: neutral or positive vs champion)

---

## Common Mistakes

| Mistake | Consequence | Prevention |
|---|---|---|
| Skipping shadow mode for critical models | Production failures affect real users | Shadow mode is mandatory for P0/P1 models |
| Not pre-calculating A/B test sample size | Test ends with inconclusive results | Calculate before starting, not after |
| Randomizing user assignment per-request | Users flip between models, contaminating results | Always hash user_id for consistent assignment |
| Not defining rollback criteria upfront | Slow, subjective rollback decisions | Define guardrails before starting any test |
| Testing multiple changes simultaneously | Cannot attribute results to any change | One variable per test |

---

**Previous:** [02 — Continuous Training](02-continuous-training.md) | **Next:** [04 — Drift Detection →](04-drift-detection.md)
