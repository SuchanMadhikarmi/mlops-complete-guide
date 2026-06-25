# 00 — Why MLOps is Different (Start Here If You're New)

> If you're a DevOps engineer reading this for the first time, this file is your most important read. It reframes everything you think you know about software deployment — because ML systems break the rules you're used to.

---

## Read This Before Anything Else

You've deployed software before. You know how it works: write code, test it, deploy it, monitor it. If it breaks, you fix the bug and redeploy. The code does what the code says.

**Machine learning doesn't work like that.**

This isn't a small difference. It's a fundamental difference in how systems behave, fail, and need to be maintained. Understanding this changes how you read everything else in this guide.

---

## The 5 Ways ML Breaks Your Mental Model

### 1. "Deploy Once, Run Forever" Doesn't Apply

**How software works:**
- You deploy version 1.0
- It runs unchanged until you change the code
- Old code keeps working unless you break something

**How ML works:**
- You train a model on data from 2024
- The model works perfectly in 2024
- In 2025, the real world changes (fraud patterns shift, user behavior changes, economic conditions change)
- Your model's accuracy drops — **with zero code changes**
- The model is now wrong about the world because the world changed

This is called **data drift**. It means an ML model has a natural expiry date. You must retrain it on fresh data, not just redeploy it.

> **DevOps analogy:** Imagine if your load balancer configuration became incorrect just because traffic patterns changed — with no configuration file being modified. That's what drift does to ML models.

---

### 2. Models Can Be Right on Average But Wrong in Ways That Matter

**How software fails:** Code either works or it doesn't. A null pointer exception is obvious. A wrong calculation is a bug you can find and fix.

**How ML fails:** A model that's "94% accurate" can still:
- Be wrong on all the edge cases that matter most
- Be systematically wrong for one group of users
- Be confident and wrong (the worst kind)
- Slowly get more wrong over time without any alert going off

There is no stack trace when a model starts drifting. It just quietly gets worse until someone notices revenue dropping or a business analyst asks "why are fraud rates up?"

> **This is why monitoring ML systems is different from monitoring software systems.** You can't just watch CPU and memory. You have to watch what the model is actually predicting.

---

### 3. Reproducing a Model is Much Harder Than Reproducing a Build

**How software reproducibility works:** Git commit + same dependencies = same binary. It's solved.

**How ML reproducibility fails:** Even with the same code and same dependencies, you can't reproduce a model if you don't have:
- The exact same training data (at the exact same version)
- The exact same random seed
- The exact same hardware (some GPU operations are non-deterministic)
- Every single hyperparameter (including defaults you didn't think to log)

This is why **experiment tracking** and **data versioning** are the first two skills in this guide. Without them, you can't answer "which exact model is in production right now, and can we recreate it?" — and that question comes up constantly in production incidents.

---

### 4. Testing ML is Harder Than Testing Software

**How you test software:** Write unit tests. Test inputs → assert outputs. Pass/fail is deterministic.

**How you test ML:**
- You can't assert that a model produces the exact right answer (it's probabilistic)
- What you test is: accuracy on held-out data, latency under load, behavior on edge cases
- But a model that passes all your tests can still be wrong after deployment if production data doesn't look like your test data
- And a model can degrade gradually — not fail suddenly — making alerting harder

> **There's no `AssertionError` for "model became 5% less accurate this month."** You need statistical tests and custom monitoring dashboards for that.

---

### 5. The Model is Only 10% of the Work

This one surprises everyone who comes from data science.

A data scientist builds a model with 94% accuracy in a Jupyter notebook. That model is maybe 10% of the production system. The other 90% is:

- Input validation (handling null values, wrong data types, out-of-range inputs)
- Feature engineering (computing features the same way in serving as in training)
- Serving infrastructure (latency SLAs, load balancing, auto-scaling)
- Model versioning (knowing which version is deployed and being able to roll back)
- Monitoring (detecting when the model starts misbehaving)
- Retraining pipelines (automatically retraining when performance drops)
- Safety mechanisms (graceful fallbacks when the model errors)
- Auditing/compliance (logging every prediction for legal requirements)

**MLOps is building and operating that other 90%.** This is exactly where DevOps skills apply.

---

## The DevOps Skills That Transfer Directly

Good news: your existing skills are highly relevant. Here's the direct mapping:

| What You Know (DevOps) | What It Becomes (MLOps) | What's Different |
|---|---|---|
| Docker containers | ML model containers | GPU support, CUDA versions, larger images |
| CI/CD pipelines | ML training pipelines | The "build" step is training a model, not compiling code |
| Config versioning (Git) | Experiment tracking (MLflow) | You also version data and hyperparameters |
| Infrastructure monitoring (CPU/memory) | Model monitoring | You also monitor prediction distributions and accuracy |
| Health checks | Model readiness checks | Must verify model loaded AND is making sane predictions |
| Rollback on failed deploy | Model rollback | Triggered by accuracy drop, not just errors |
| Feature flags / canary deploys | Shadow deploys / A/B testing | The evaluation criteria are statistical, not just "is it up?" |
| Log everything | Log all experiment details | Must log data hash, random seeds, every hyperparameter |

**The conceptual skills are identical.** You understand reliability, reproducibility, observability, and automation. You just need to learn the ML-specific tooling and failure modes on top of that foundation.

---

## The Skills You Need to Add

The gaps are smaller than you think. You need to understand:

1. **Statistical concepts** — What is PSI? What is a p-value? What does "distribution shift" mean numerically? (Covered in `supporting-knowledge/01-statistics-for-mlops.md`)

2. **ML-specific failure modes** — Concept drift vs data drift vs label drift. Training-serving skew. Why `model.eval()` matters. (Covered in `ml-fundamentals/`)

3. **ML tooling** — MLflow, DVC, Evidently, Feast, KubeFlow Pipelines. These sit on top of Kubernetes and Docker, which you already know. (Covered in `core-mlops/` and `production-engineering/`)

That's it. None of these are harder than what you already know. They're just unfamiliar.

---

## The Three Mental Shifts to Make Right Now

Before you read another file in this guide, internalize these:

**Mental shift 1: Models expire.**
Every model has an implicit expiry date. Your job is to detect when it's happening and retrain before the business notices.

**Mental shift 2: Silence is not success.**
A model that doesn't error is not necessarily working correctly. Silent accuracy degradation is the most common ML production incident. Monitoring must go deeper than "is the service up?"

**Mental shift 3: Data is a first-class artifact.**
In software, the code is the artifact. In ML, the code AND the data are artifacts. You need version control for both. Losing the training data version is as bad as losing the code version — you can't reproduce the model.

---

## What Comes Next

Now that you have the right mental model, the rest of this guide will make much more sense:

1. **`ml-fundamentals/`** — How models actually learn, what loss functions are, what training failure looks like. Don't skip this even if you think it's too basic — the production implications are not obvious.

2. **`GLOSSARY.md`** — Reference for any term you don't recognize. Skim it now, use it as a lookup later.

3. **`core-mlops/`** — The tools every production ML team uses: MLflow for experiment tracking, DVC for data versioning, FastAPI for serving, and CI/CD for automated pipelines.

4. **`production-engineering/`** — The layer above the core stack: feature stores, continuous training, drift detection, safe deployment strategies.

---

**Next:** [01 — How Models Actually Learn →](01-how-models-learn.md)
