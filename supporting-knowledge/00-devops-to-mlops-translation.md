# 00 — DevOps to MLOps: Your Translation Guide

> You already know 60% of MLOps. This file maps what you know to what you need to learn, so you stop reading new concepts as foreign and start reading them as extensions of what you already do.

---

## 📚 Prerequisites

This guide assumes you already know:
- ✅ Docker (build, run, push, multi-stage builds)
- ✅ CI/CD pipelines (GitHub Actions, Jenkins, or similar)
- ✅ Basic monitoring (CPU, memory, uptime, alerting)
- ✅ Version control with Git
- ✅ Kubernetes basics (deployments, services, health checks)

If you're missing any of these, check `practical-skills/` first.

---

## The Master Translation Table

| DevOps Concept | MLOps Equivalent | Same Idea? | Key Difference |
|---|---|---|---|
| Docker image | ML serving container | ✅ Same tool | GPU support needed, images 5-15GB vs 100MB |
| `docker build` | Model training job | ⚠️ Somewhat | Output is a trained model, not a binary |
| `git commit` | MLflow run | ⚠️ Somewhat | Logs data version + hyperparams, not just code |
| Git repository | MLflow experiment | ⚠️ Somewhat | Contains runs (training attempts), not code files |
| Artifact registry | Model registry (MLflow) | ✅ Same idea | Stores model versions with staging/prod/archived lifecycle |
| Config file (.yaml) | Hyperparameters | ✅ Same idea | Must be logged for every training run |
| Config versioning | Data versioning (DVC) | ⚠️ Somewhat | Data is 100GB+, needs a different tool than Git |
| CI/CD pipeline | ML training pipeline | ✅ Same concept | The "build" step trains a model instead of compiling code |
| Unit tests | ML model tests | ⚠️ Somewhat | Can't assert exact outputs — test accuracy and behavior |
| Health check `/health` | Liveness probe | ✅ Same thing | "Is the process running?" |
| Readiness check `/ready` | Readiness probe | ✅ Same idea | "Is the model loaded and ready to serve?" |
| CPU/memory monitoring | Infrastructure monitoring | ✅ Same tools | Use Prometheus + Grafana exactly the same way |
| Business metric monitoring | Model performance monitoring | ❌ New concept | Monitor prediction accuracy + distribution |
| Rollback on deploy failure | Rollback on accuracy drop | ⚠️ Somewhat | Trigger is different — not an error, but statistical |
| Feature flag | Shadow deployment / canary | ✅ Same idea | Route % of traffic to new model version |
| A/B test (software) | Champion-challenger test | ✅ Same concept | Evaluation is statistical, not just "is it up?" |
| Log every request | Log every prediction | ✅ Same discipline | Also log input features + model version + latency |

---

## Deep Dives: The 6 Most Important Translations

### 1. Git → Experiment Tracking (MLflow)

**What you know:** You commit code to Git. Every commit has a hash, a message, and a diff. You can check out any historical commit.

**What's new:** In ML, you're not just versioning code. You're versioning a *training run* — which includes:
- The code (git commit hash)
- The data (DVC hash of training dataset)
- Every hyperparameter (learning rate, model architecture, etc.)
- The results (accuracy, loss, metrics)
- The output artifact (the trained model file)

Git doesn't handle this because a "training run" involves gigabytes of data and model files that Git can't version. **MLflow is the tool that logs all of this for every training run.**

```
Git commit = "I changed this code"
MLflow run = "I trained a model with these params on this data and got these metrics"
```

Without MLflow (or equivalent), you cannot answer: "What exact configuration produced the model in production?" — and you'll need to answer that every time an incident happens.

---

### 2. Config Files → Hyperparameters

**What you know:** Your apps have config files (`.yaml`, `.env`) that control behavior. You version them and change them for different environments.

**What's new:** ML models also have "config" — called **hyperparameters**. These are values you set before training that control *how* the model learns:
- `learning_rate: 0.01` — how big of a step to take when updating the model
- `n_estimators: 300` — how many decision trees to build
- `batch_size: 32` — how many training examples to process at once
- `max_depth: 6` — how complex each decision tree is allowed to be

**The critical difference:** Hyperparameters don't just configure the software. They determine the model's accuracy. Two models trained with different hyperparameters on the same data can have very different performance.

**The discipline required:** You must log *all* hyperparameters for every training run — including the defaults you didn't change. If you only log `n_estimators: 300` but forget to log `max_depth: 6`, you cannot reproduce that model.

---

### 3. Data Version Control (DVC) vs Git

**What you know:** Git versions code. You can `git checkout abc123` to get any historical version.

**The problem:** Training data is typically gigabytes or terabytes. Git breaks at 100MB. You can't `git add data/train.parquet` for a 50GB dataset.

**What DVC does:** DVC stores a tiny *pointer file* (just a hash) in Git, while the actual data lives in S3/GCS/local storage. When you run `dvc checkout`, DVC downloads the exact version of the data that matches your Git commit.

```
Git repo contains:       data/train.parquet.dvc  (50 bytes, just a hash)
S3/MinIO contains:       data/train_abc123.parquet  (50 GB, actual data)

git checkout <commit>    → gets the .dvc pointer file
dvc checkout             → downloads the matching 50GB file from S3
```

Result: `git checkout <commit> && dvc checkout` gives you the exact code + exact data from any point in history. True reproducibility.

---

### 4. CI/CD Pipeline → ML Training Pipeline

**What you know:** CI/CD runs on every commit: lint → test → build → push → deploy.

**What an ML pipeline looks like:** trigger → validate data → train model → evaluate → register → deploy.

```
CI/CD (Software):
Push code → Run tests → Build Docker image → Push to registry → Deploy

ML Pipeline:
New data arrives → Validate data quality → Train model →
    Evaluate: does new model beat old model? →
    If yes: Register in MLflow → Deploy to production
    If no: Alert team, keep old model
```

**The key difference in the "test" step:** In software CI, tests pass or fail deterministically. In ML pipelines, the evaluation step compares the new model against the current production model using statistical metrics. "Does this model beat the current champion by more than 0.5% AUC?" is the ML equivalent of passing tests.

**The "quality gate"** (step 4: Evaluation Gate) is the most important part. It ensures you never deploy a model that's worse than what's already in production — even if the training run completed successfully.

---

### 5. Infrastructure Monitoring → ML Model Monitoring

**What you know:** You monitor CPU, memory, disk, network, latency, error rates. Prometheus scrapes metrics. Grafana visualizes them. PagerDuty alerts when things are wrong.

**What you still do:** All of the above. Identical. Use the same Prometheus + Grafana stack.

**What you add on top:**

| New Metric | What It Measures | Alert When |
|---|---|---|
| Prediction distribution | Are predictions shifting? (more fraud than usual?) | Distribution shifts significantly |
| Feature distribution | Are input features changing? | PSI > 0.2 on key features |
| Model accuracy (if labels available) | Is the model still right? | Accuracy drops below threshold |
| Prediction latency (P99) | Is inference fast enough? | P99 > SLA (e.g., 200ms) |
| Fallback rate | How often is the model erroring? | Fallback > 1% of requests |

The tools are the same. The metrics are different. You're monitoring the model's behavior on data, not just the infrastructure's resource usage.

---

### 6. Rollback → Model Rollback

**What you know:** If a deployment causes errors, you rollback. In Kubernetes: `kubectl rollout undo deployment/myapp`. In 30 seconds, you're back to the previous version.

**How ML rollback is the same:** You keep the previous model version in the MLflow registry (archived, not deleted). If the new model has problems, you can reload the archived version and serve it.

**How ML rollback is different:** You might roll back not because of an error, but because of accuracy degradation. The model runs fine — no crashes, no 500 errors — but predictions are slowly getting worse. This is harder to detect and requires:
- Monitoring prediction distributions (not just error rates)
- Setting accuracy thresholds with alerting
- Having a clear process for "when do we roll back?"

> **The scariest ML bug:** A model that is running, handling 100% of requests, returning HTTP 200, logging everything correctly — and giving increasingly wrong predictions that nobody notices for 3 weeks.

---

## The New Vocabulary (Quick Reference)

| Term | Plain English | DevOps Equivalent |
|---|---|---|
| **Training run** | One attempt at fitting a model | One CI/CD pipeline execution |
| **Hyperparameter** | Configuration that controls training | Config file value |
| **Epoch** | One complete pass through training data | One iteration in a loop |
| **Loss** | How wrong the model is during training | Test failure count (but continuous) |
| **Gradient** | Direction to adjust weights to reduce loss | Direction to change config to fix issue |
| **Overfitting** | Model memorized training data, fails on new data | Works in staging, breaks in production |
| **Data drift** | Input data distribution changed from training time | Config drift between environments |
| **Concept drift** | The relationship between inputs and outputs changed | Business logic changed but code didn't |
| **Champion** | Current production model | Current production deployment |
| **Challenger** | Newly trained model being evaluated | New version in staging |
| **Feature store** | Centralized feature computation and serving | Config management for ML features |
| **Inference** | Using a trained model to make predictions | Serving requests to an API |
| **Artifact** | Model file, plots, reports produced by training | Build artifact (binary, Docker image) |
| **Experiment** | Group of related training runs | GitHub Actions workflow |
| **Model registry** | Versioned store for trained models | Docker registry / artifact repository |
| **PSI** | Statistic measuring distribution shift | Like a diff but for data distributions |

---

## What to Learn in What Order

Given your DevOps background, here's the optimal path:

**Week 1-2: ML Fundamentals (don't skip)**
Read `ml-fundamentals/` fully. Focus on:
- How does a model actually learn? (The training loop)
- What is overfitting and why does it matter in production?
- What metrics matter for what problems?
- Why does `model.eval()` matter?

**Week 3-4: Experiment Tracking (MLflow)**
You'll recognize this as "Git + CI/CD for training runs." It clicks fast for DevOps engineers.
Read `core-mlops/01-experiment-tracking.md`.

**Week 5-6: Data Versioning (DVC)**
Think of it as "Git LFS but with ML-specific features." Straightforward.
Read `core-mlops/02-data-versioning.md`.

**Week 7-8: Model Serving (FastAPI)**
You already know how to build APIs. The new parts are: input validation for ML, `model.eval()`, graceful fallbacks, and model versioning in the response.
Read `core-mlops/03-model-serving.md`.

**Week 9-12: CI/CD for ML + Monitoring**
Almost identical to what you know. The new parts are the evaluation gate and model-specific metrics.
Read `core-mlops/04-cicd-for-ml.md` and `core-mlops/05-monitoring-basics.md`.

**After that:** Production Engineering — feature stores, continuous training, drift detection. This is where your DevOps skills really shine.

---

## The Projects That Build Your Skills Fastest

For a DevOps engineer specifically, these three projects give the fastest return:

| Project | Why It's Good for DevOps Engineers |
|---|---|
| **P-03: Production Serving API** | Uses all your Docker + Kubernetes skills. New: model loading, model.eval(), graceful fallback, model version tracking |
| **P-04: ML CI/CD Pipeline** | You already know GitHub Actions. New: the training step, the champion-challenger evaluation gate |
| **P-05: ML Observability Dashboard** | You already know Prometheus + Grafana. New: model-specific metrics (prediction distribution, drift) |

Build these three and you've closed 80% of the gap between DevOps and MLOps.

---

**Next:** [01 — How Models Actually Learn →](../ml-fundamentals/01-how-models-learn.md)  
**Or jump to tools:** [Core MLOps Stack →](../core-mlops/01-experiment-tracking.md)
