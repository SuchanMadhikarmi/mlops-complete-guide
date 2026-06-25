# 01 -- MLOps Interview Guide

## Prerequisites

**What you should know before interviewing:** Have actually built and shipped at least 2 complete ML systems to production (not just in notebooks). Know what "production" really means -- deployments that failed at 3am, on-call responsibilities, real users affected.

**Mindset for success:** Interviewers are looking for depth AND breadth. You need the depth (specific technical knowledge of MLOps patterns) and the breadth (understandi how your choices affect business metrics, infrastructure costs, team velocity).

> MLOps interviews test whether you've actually built and operated these systems -- not just read about them. Specific examples beat vague knowledge every time.

## Why This Matters (The Hiring Manager's Perspective)

MLOps engineers are expensive ($150k-$300k+/year). Companies need confidence you'll actually add value, not create more problems. This guide is their evaluation framework.

---

## The 5 Interview Stages

| Stage | Duration | Focus | How to Prepare |
|---|---|---|---|
| Recruiter Screen | 30 min | Background, salary, availability | 2-min career story with impact numbers |
| Technical Phone Screen | 45-60 min | MLOps concepts, your experience | Specific examples from real projects |
| System Design | 60 min | Design a full ML system from a problem | Practice the 4-question framework |
| Coding | 45-60 min | ML-flavored coding (not LeetCode) | FastAPI serving, PSI, data validation |
| Behavioral | 30-45 min | STAR format stories | 3 stories prepared: incident, disagreement, complex system |

---

## System Design: The 4 Questions First

Before drawing ANY architecture, ask and answer these:

```
1. Prediction target  → What exactly is the model predicting? Binary? Score? Ranking?
                         This determines model type and evaluation metrics.

2. Latency           → Does it need to respond in 50ms, 5 seconds, or can it run overnight?
                         This is the MOST important architectural question.
                         Determines: batch vs real-time, feature store design, model complexity.

3. Scale             → How many predictions per second? How many unique entities?
                         Determines: serving infra, feature store backend, distributed training needs.

4. Feedback loop     → How and when do you know if predictions were correct?
                         Determines: CT feasibility, training data freshness, label latency.
```

---

## Top Interview Questions + Ideal Answers

### "How do you detect when a model needs retraining?"

```
Answer framework (mention all 3 signals):

1. Drift-based (proactive): Monitor PSI on key input features.
   PSI > 0.2 → trigger retraining. This is a LEADING indicator --
   you act before performance degrades.

2. Performance-based (reactive): Monitor proxy online metrics
   (CTR, conversion, fraud catch rate). Drop below threshold → retrain.
   Requires a feedback loop that labels arrive quickly enough.

3. Time-based (fallback): Scheduled retraining every N days
   regardless. Simple, predictable, handles slow drift.

Production implementation: Prefect/Airflow DAG that checks all 3
signals daily. Triggers CT pipeline automatically. Posts Slack alert.
```

### "How do you deploy a model with zero downtime?"

```
Shadow deployment → Canary → Full promotion.

Shadow: new model runs on 100% of traffic, predictions are logged
but NEVER served. Zero user risk. Run for 24-72h.
→ Learn: latency, errors, edge cases, where models disagree.

Canary: 5% → 25% → 50% → 100% traffic shift.
Wait at each stage. Check error rate, latency P99, business metrics.
Rollback config: change one YAML file, takes 30 seconds, no code change.

Automatic rollback: if error rate > 2% or P99 > 150ms for 10 minutes
→ automatically revert to champion (AlertManager → webhook → routing config update).
```

### "What's the difference between data drift and concept drift?"

```
Data drift (covariate shift): P(X) changes -- input distribution changes.
Example: platform expands to new country, demographic is different.
The model-world relationship (P(Y|X)) is still valid, just applied to
different inputs.
Response: retrain with representative data.

Concept drift: P(Y|X) changes -- the relationship itself changes.
Example: fraud patterns fundamentally change after a major regulatory shift.
Retraining on new data with old features won't fully fix this.
Response: investigate features, possibly redesign feature engineering.

Treating concept drift as data drift wastes weeks retraining without improvement.
Always identify WHICH type before prescribing a response.
```

### "How do you ensure experiment reproducibility?"

```
5 ingredients, all logged automatically on every run:

1. Code version: git commit hash (subprocess git rev-parse HEAD)
2. Data version: DVC hash of training dataset
3. Environment: requirements.txt + Docker image digest
4. All hyperparameters: model.get_params() -- logs defaults too
5. Random seeds: Python, NumPy, PyTorch -- all explicitly set and logged

Auto-logged in training wrapper:
  mlflow.log_params({
    "git_commit": git_hash,
    "data_version": dvc_hash,
    "random_seed": 42,
    **model.get_params()
  })

Result: any run can be reproduced exactly by anyone with repo access.
```

---

## Coding Round Examples

```python
# Common coding questions:

# 1. Compute PSI between two distributions
def compute_psi(expected, actual, buckets=10):
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    exp_pct = np.histogram(expected, bins=breakpoints)[0] / len(expected)
    act_pct = np.histogram(actual, bins=breakpoints)[0] / len(actual)
    exp_pct = np.where(exp_pct == 0, 0.0001, exp_pct)
    act_pct = np.where(act_pct == 0, 0.0001, act_pct)
    return float(np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct)))

# 2. FastAPI model serving endpoint
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = load_model()

class Request(BaseModel):
    features: list[float]

@app.post("/predict")
async def predict(req: Request):
    prob = float(model.predict_proba([req.features])[0, 1])
    return {"probability": prob}

# 3. Detect data leakage
def check_for_leakage(df, target_col, threshold=0.99):
    for col in df.columns:
        if col == target_col:
            continue
        corr = abs(df[col].corr(df[target_col]))
        if corr > threshold:
            print(f"LEAKAGE ALERT: {col} correlates {corr:.3f} with {target_col}")
```

---

## Behavioral Round Stories (STAR Format)

Prepare one story for each:

**Incident story:** "Tell me about a time a model failed in production"
- Situation: what system, what happened, what was the impact
- Task: your responsibility in resolving it
- Action: how you diagnosed and fixed it (be specific about commands/process)
- Result: how quickly resolved, what you implemented to prevent recurrence

**Disagreement story:** "Tell me about a disagreement with a data scientist"
- Frame as: they wanted to do X, you identified Y risk, you proposed Z
- Never make the data scientist the villain
- Show that you were collaborative and used data to make the case

**Complex system story:** "Walk me through the most complex ML system you've built"
- Use the 4-question framework to describe it
- Cover: what you chose and why (tradeoffs), what you'd do differently

---

## Salary Benchmarks (USD, Remote)

| Role | Experience | Salary Range |
|---|---|---|
| Junior MLOps Engineer | 0-2 years | $60k-$90k |
| Mid MLOps Engineer | 2-5 years | $100k-$140k |
| Senior MLOps Engineer | 5+ years | $140k-$180k |
| Staff / Principal | 8+ years | $180k-$250k+ |
| ML Platform Lead | 10+ years | $200k-$300k+ |

Nepal-based with remote USD role: $30k-$80k is realistic at 2-5 years experience. Top 0.1% tier: $80k-$150k+ remote.

---

**Next:** [02 -- Portfolio Strategy →](02-portfolio-strategy.md)
