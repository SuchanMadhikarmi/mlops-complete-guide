#!/usr/bin/env python3
"""
MLOps Complete Guide -- Master Setup Script
==========================================
Run this script inside an empty folder to generate the complete repo.
Usage: python setup.py

Author: Suchan Madhikarmi
"""

import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))
    print(f"  created  {path}")

print("\n🚀 Building MLOps Complete Guide repository...\n")

# ─────────────────────────────────────────────────────────────────────────────
# DIRECTORIES
# ─────────────────────────────────────────────────────────────────────────────
for d in [
    "ml-fundamentals", "core-mlops", "production-engineering",
    "advanced-specialized", "llmops", "supporting-knowledge",
    "practical-skills", "career", "projects", "assets",
]:
    os.makedirs(d, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# README
# ─────────────────────────────────────────────────────────────────────────────
write("README.md", """
<div align="center">

# 🚀 MLOps Complete Guide
### From DevOps Engineer to Top 0.1% MLOps Professional

[![Stars](https://img.shields.io/github/stars/SuchanMadhikarmi/mlops-complete-guide?style=for-the-badge&color=00d4a8)](https://github.com/SuchanMadhikarmi/mlops-complete-guide/stargazers)
[![Forks](https://img.shields.io/github/forks/SuchanMadhikarmi/mlops-complete-guide?style=for-the-badge&color=3b82f6)](https://github.com/SuchanMadhikarmi/mlops-complete-guide/network)
[![License: MIT](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-e84393?style=for-the-badge)](CONTRIBUTING.md)

<br/>

**The most complete, practical MLOps knowledge base on GitHub.**
Built from real production experience. Written for engineers, by an engineer.
No fluff. No paywalls. Everything you need -- from ML fundamentals to top 0.1%.

<br/>

[📖 Start Reading](#-how-to-use-this-guide) &nbsp;·&nbsp; [🗺️ Roadmap](#-learning-roadmap) &nbsp;·&nbsp; [💼 Projects](#-portfolio-projects) &nbsp;·&nbsp; [🤝 Contribute](CONTRIBUTING.md)

</div>

---

## 👋 Who This Is For

| You are... | This helps you... |
|---|---|
| **DevOps / SRE engineer** | Leverage your infra skills to transition into MLOps |
| **Software engineer** | Understand ML systems end-to-end in production |
| **Data scientist** | Understand the platform and infrastructure around your models |
| **Student** | Get a structured, production-focused learning path |
| **Hiring manager** | Understand what a strong MLOps engineer actually knows |

No ML PhD required. Production experience over theory. Real examples throughout.

---

## 📊 What's Inside

| # | Section | Topics |
|---|---|---|
| 01 | 🧠 ML Fundamentals | How models learn, model types, metrics, data |
| 02 | ⚙️ Core MLOps Stack | MLflow, DVC, FastAPI serving, CI/CD, monitoring |
| 03 | 🏭 Production Engineering | Feature stores, CT pipelines, drift, shadow/canary |
| 04 | 🔬 Advanced & Specialized | Distributed training, K8s ML, compression, Triton |
| 05 | 🤖 LLMOps | RAG, fine-tuning, observability, guardrails, vLLM |
| 06 | 📐 Supporting Knowledge | Statistics, data engineering, cloud platforms, security |
| 07 | 🔧 Practical Skills | Docker, Kubernetes, testing, debugging, SQL, async |
| 08 | 💼 Career | Interview guide, portfolio strategy, outreach templates |
| 09 | 🎯 Projects | 10 graded portfolio projects with full specs |

**35+ comprehensive guides · 100+ concepts · Production-grade code examples**

---

## 🗺️ Learning Roadmap

```
┌────────────────────────────────────────────────────────────────┐
│  PHASE 0 (4-6 wk)   PHASE 1 (8-10 wk)   PHASE 2 (10-12 wk)  │
│  Foundations     →  Core Stack        →  Production           │
│                                                                │
│  Python · SQL       MLflow · DVC          Feature Stores      │
│  ML basics          FastAPI serving       Continuous Training  │
│  Docker · K8s       GitHub Actions CI     Shadow/Canary       │
│  Statistics         Prometheus/Grafana    Drift Detection     │
├────────────────────────────────────────────────────────────────┤
│  PHASE 3 (12-16 wk)              PHASE 4 (ongoing)            │
│  Advanced                        Top 0.1%                     │
│                                                                │
│  Distributed Training            Open Source Contribution     │
│  Kubernetes-Native ML            Technical Blog Writing       │
│  Model Compression               LLMOps Engineering           │
│  Multi-Model Serving (Triton)    ML Platform Architecture     │
└────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
mlops-complete-guide/
│
├── 📂 ml-fundamentals/
│   ├── 01-how-models-learn.md        ← Training loop, loss, weights, LR
│   ├── 02-model-types.md             ← Trees, NNs, Transformers + MLOps profiles
│   ├── 03-evaluation-metrics.md      ← Every metric explained with examples
│   └── 04-data-fundamentals.md       ← Leakage, splits, imbalance, features
│
├── 📂 core-mlops/
│   ├── 01-experiment-tracking.md     ← MLflow complete guide + W&B
│   ├── 02-data-versioning.md         ← DVC + Great Expectations
│   ├── 03-model-serving.md           ← FastAPI production template
│   ├── 04-cicd-for-ml.md             ← GitHub Actions ML pipelines
│   └── 05-monitoring-basics.md       ← Prometheus + Grafana for ML
│
├── 📂 production-engineering/
│   ├── 01-feature-stores.md          ← Feast + Redis, point-in-time
│   ├── 02-continuous-training.md     ← CT triggers, 7-step pipeline
│   ├── 03-safe-deployments.md        ← Shadow, A/B, canary rollouts
│   ├── 04-drift-detection.md         ← PSI, SHAP drift, 3 types
│   ├── 05-model-explainability.md    ← SHAP + LIME complete guide
│   └── 06-inference-patterns.md      ← Batch vs real-time vs streaming
│
├── 📂 advanced-specialized/
│   ├── 01-distributed-training.md    ← Ray, DeepSpeed, ZeRO
│   ├── 02-kubernetes-native-ml.md    ← KFP, Argo Workflows
│   ├── 03-model-compression.md       ← Quantization, ONNX, distillation
│   ├── 04-multi-model-serving.md     ← NVIDIA Triton complete guide
│   └── 05-platform-design.md         ← ML platform patterns, build vs buy
│
├── 📂 llmops/
│   └── 01-llmops-complete.md         ← RAG, fine-tuning, observability
│
├── 📂 supporting-knowledge/
│   ├── 01-statistics-for-mlops.md    ← Hypothesis testing, PSI, CI
│   ├── 02-data-engineering.md        ← Kafka, medallion arch, Spark
│   ├── 03-cloud-platforms.md         ← SageMaker vs Vertex AI vs Azure ML
│   ├── 04-ml-security.md             ← Poisoning, adversarial, privacy
│   ├── 05-design-patterns.md         ← Two-Tower, Bandit, Embeddings
│   └── 06-python-ecosystem.md        ← NumPy, Pandas, sklearn, PyTorch
│
├── 📂 practical-skills/
│   ├── 01-docker-for-ml.md           ← GPU containers, CUDA, multi-stage
│   ├── 02-kubernetes-for-ml.md       ← GPU resources, PVCs, Jobs
│   ├── 03-testing-ml-systems.md      ← 4 levels of ML testing
│   ├── 04-debugging-ml.md            ← Systematic debugging guide
│   ├── 05-sql-for-mlops.md           ← Aggregations, window functions
│   └── 06-async-python.md            ← async/await, Pydantic, caching
│
├── 📂 career/
│   ├── 01-interview-guide.md         ← 5 interview stages, system design
│   └── 02-portfolio-strategy.md      ← GitHub, blog, outreach templates
│
├── 📂 projects/
│   └── 10-portfolio-projects.md      ← Full specs for all 10 projects
│
├── 📄 QUICK-REFERENCE.md             ← Checklists, commands, tables
├── 📄 CONTRIBUTING.md
└── 📄 LICENSE
```

---

## 🎯 Portfolio Projects

| # | Project | Stack | Level | Impact |
|---|---|---|---|---|
| P-01 | Full MLflow Pipeline on Docker | MLflow · PostgreSQL · MinIO | 🟢 Foundation | ⭐⭐⭐⭐ |
| P-02 | Versioned Data Pipeline with DVC | DVC · Great Expectations | 🟢 Foundation | ⭐⭐⭐⭐⭐ |
| P-03 | Production Model Serving API | FastAPI · MLflow · K8s · Prometheus | 🟢 Foundation | ⭐⭐⭐⭐⭐⭐ |
| P-04 | Automated ML CI/CD Pipeline | GitHub Actions · MLflow · Docker | 🔵 Core | ⭐⭐⭐⭐⭐⭐⭐ |
| P-05 | ML Observability Dashboard | Grafana · Prometheus · Evidently | 🔵 Core | ⭐⭐⭐⭐⭐⭐⭐ |
| P-06 | Automated Continuous Training | Prefect · MLflow · Evidently · K8s | 🔵 Core | ⭐⭐⭐⭐⭐⭐⭐⭐ |
| P-07 | Shadow + Canary Deployment | Traefik · FastAPI · Redis | 🟡 Advanced | ⭐⭐⭐⭐⭐⭐⭐⭐ |
| P-08 | Feature Store (Online + Offline) | Feast · Redis · Kafka · PostgreSQL | 🟡 Advanced | ⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| P-09 | Kubernetes-Native ML Pipeline | KubeFlow Pipelines · Argo · Ray | 🔴 Elite | ⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| P-10 | Mini ML Platform (End-to-End) | Everything above + Terraform + Helm | 🔴 Elite | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |

---

## 🔑 The 10 Things Most Engineers Don't Know

1. **Data versioning matters more than model versioning** -- if you can't reproduce the training data, you can't reproduce the model
2. **The NIPS 2015 paper** "Hidden Technical Debt in ML Systems" names every production failure mode you'll face
3. **3 types of drift need 3 different responses** -- treating concept drift as data drift wastes weeks
4. **Shadow mode before A/B** -- always test on real traffic with zero user risk first
5. **The gap between working and production is 10x** -- the model is the easy part
6. **Feature stores are the rarest skill** -- Feast + Redis knowledge opens doors others can't get through
7. **model.eval() is non-negotiable** -- forgetting it leaves dropout active and predictions non-deterministic
8. **Batch size = GPU memory** -- OOM error means reduce batch size first
9. **Never put secrets in code** -- git history is permanent
10. **Overlapping confidence intervals = no winner** -- don't call A/B tests early

---

## 📚 How to Use This Guide

**If you're starting MLOps:** Begin at `ml-fundamentals/` → `core-mlops/` → build Projects P-01 to P-03

**If you're transitioning from DevOps:** Jump to `core-mlops/` → focus on `production-engineering/` → build P-03, P-04, P-05

**For interviews:** Read `career/01-interview-guide.md` first → study `production-engineering/` → practice system design

**For quick answers:** `QUICK-REFERENCE.md` has all checklists, commands, and comparison tables

---

## ⭐ Support This Project

If this guide helped you -- **star it, share it, and tag me on LinkedIn.**

Every star helps other engineers find this resource. Every share might help someone land their dream MLOps role.

---

## 👤 Author

**Suchan Madhikarmi** -- DevOps → MLOps Engineer, Kathmandu, Nepal

- 🌐 [suchanmadhikarmi.com.np](https://suchanmadhikarmi.com.np)
- 💼 [linkedin.com/in/suchanmadhikarmi](https://linkedin.com/in/suchanmadhikarmi)
- 🐙 [github.com/SuchanMadhikarmi](https://github.com/SuchanMadhikarmi)

---

## 📄 License

MIT License -- free to use, share, and build upon. See [LICENSE](LICENSE).
""")

# ─────────────────────────────────────────────────────────────────────────────
# ML FUNDAMENTALS
# ─────────────────────────────────────────────────────────────────────────────
write("ml-fundamentals/01-how-models-learn.md", """
# 01 -- How Models Actually Learn

> Every model -- from simple fraud detection to GPT-4 -- follows the same 4-step loop. Understand this deeply and you can debug any training failure.

---

## The Training Loop

```
Step 1: Make Prediction  →  Step 2: Measure Error (Loss)
                                          ↓
Step 4: Update Weights   ←  Step 3: Compute Gradient Direction

Repeat millions of times → model learns
```

### Step 1 -- Prediction
Model takes input features, produces an output. Initially random -- knows nothing.

### Step 2 -- Loss (How Wrong Are We?)
A mathematical function measures the gap between prediction and correct answer.

| Loss Function | Task | Key Property |
|---|---|---|
| Binary Cross-Entropy | Binary classification | Penalizes confident wrong predictions |
| Categorical Cross-Entropy | Multi-class | One-vs-all |
| MSE | Regression | Squares errors -- large errors penalized more |
| Focal Loss | Imbalanced classification | Focuses on hard examples |

### Step 3 -- Gradient (Which Direction?)
Backpropagation calculates: "For each weight, if I increase it slightly, does loss go up or down?"

### Step 4 -- Update Weights
```
new_weight = old_weight - learning_rate × gradient
```

---

## The Learning Rate

```
Too HIGH:  Loss bounces wildly → never converges
Too LOW:   Training takes forever / never finishes
Just RIGHT: Smooth decrease → good solution
```

**MLOps signal:** "Training isn't converging" → check learning rate first.

---

## Batch Size → GPU Memory

```python
# Batch size controls GPU memory consumption directly
batch_size = 32    # baseline
batch_size = 64    # ~2x memory
batch_size = 128   # ~4x memory

# OOM (Out of Memory) error fix: reduce batch size
# Slow training fix: increase batch size (with LR scaling)
```

---

## Critical Production Rules

```python
# Rule 1: ALWAYS call model.eval() before inference
model.eval()                        # disables dropout → deterministic predictions
with torch.no_grad():               # saves memory, faster
    prediction = model(input)

# Forgetting model.eval() = dropout stays active = different prediction every call

# Rule 2: Log 5 things in every training run
mlflow.log_params({
    "git_commit":    get_git_hash(),      # code version
    "data_version":  get_dvc_hash(),      # data version
    "random_seed":   42,                  # random seed
    "docker_image":  "training:v3",       # environment
})
mlflow.log_params(model.get_params())     # ALL hyperparameters
```

---

## Training Failure Diagnosis

| Symptom | First Cause to Check | Fix |
|---|---|---|
| Loss = NaN | LR too high or NaN in data | Reduce LR 10x, validate data |
| Loss not decreasing | LR too low | Increase LR |
| Val loss >> train loss | Overfitting | More data, regularization, early stop |
| Both losses high | Underfitting | More complex model, better features |
| Non-deterministic predictions | `model.eval()` not called | Add `model.eval()` before serving |
| Loss spikes suddenly | Learning rate too high | Add gradient clipping |

---

**Next:** [02 -- Model Types →](02-model-types.md)
""")

write("ml-fundamentals/02-model-types.md", """
# 02 -- Model Types

> You need to know what each model type costs to serve, how it fails, and what infrastructure it needs.

---

## Gradient Boosting (XGBoost, LightGBM, CatBoost)

**The production workhorse for tabular data.** Builds trees sequentially -- each one corrects errors of previous trees.

```
Round 1: 70% right, 30% wrong
Round 2: New tree focuses on the 30% → 85% right
Round 3: New tree focuses on remaining errors → 91% right
...100 rounds later → 97% right
```

**MLOps Profile:**
- Training: CPU/GPU, minutes to hours
- Inference: CPU, **milliseconds** -- thousands/second
- Memory: MB to low GB
- GPU at serving: **never needed**
- ONNX export: fully supported

**When to use:** Any tabular/structured data. Always start here before trying neural networks.

---

## Neural Networks (Feedforward)

Layers of connected neurons. Each layer transforms input through: `output = activation(weights × input + bias)`

```python
# PyTorch -- Critical production pattern
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(20, 128), nn.ReLU(),
            nn.Dropout(0.3),            # ← training only!
            nn.Linear(128, 1), nn.Sigmoid()
        )

# Training:
model.train()    # dropout ACTIVE
output = model(X)

# Serving -- ALWAYS:
model.eval()     # dropout DISABLED -- deterministic predictions
with torch.no_grad():
    output = model(X)
```

**MLOps Profile:**
- Training: GPU, hours
- Inference: CPU/GPU, 1-50ms
- Key danger: forgetting `model.eval()`

---

## CNNs (Convolutional)

Specialized for images and spatial data. Filters slide across input detecting local patterns.

**MLOps Profile:**
- GPU required for training AND serving at scale
- Production optimization: PyTorch → ONNX → TensorRT (3-10x speedup)
- Batching critical for GPU utilization

---

## Transformers

Self-attention reads every token in context of all others. Powers BERT, GPT, Claude, LLaMA.

**Memory requirements:**
| Parameters | FP32 | FP16 | INT8 | INT4 |
|---|---|---|---|---|
| 7B | 28 GB | 14 GB | 7 GB | 3.5 GB |
| 70B | 280 GB | 140 GB | 70 GB | 35 GB |

**MLOps Profile:**
- GPU strongly preferred
- KV-cache essential for inference speed
- vLLM for high-throughput serving

---

## Model Selection Guide

```
What type of data?
├── Tabular (spreadsheet-like)   → Start with LightGBM
├── Images                        → CNN or Vision Transformer
├── Text / Language               → Transformer (BERT/GPT variants)
├── Time-series                   → XGBoost with lag features OR LSTM
└── Ultra-low latency needed      → Logistic Regression
```

---

## MLOps Infrastructure by Model Type

| Model | Serving | Instance | Typical Latency |
|---|---|---|---|
| sklearn / LightGBM | FastAPI + ONNX Runtime | CPU 2-4 core | 1-10ms |
| PyTorch CNN | Triton + TensorRT | GPU T4+ | 10-50ms |
| BERT-base | FastAPI + ONNX | GPU preferred | 50-200ms |
| LLM 7B | vLLM | GPU A10G+ | 500ms-2s |
| LLM 70B | vLLM multi-GPU | Multi A100 | 1-5s |

---

**Next:** [03 -- Evaluation Metrics →](03-evaluation-metrics.md)
""")

write("ml-fundamentals/03-evaluation-metrics.md", """
# 03 -- Evaluation Metrics

> Every metric answers one specific question. Choosing the wrong metric optimizes for the wrong thing.

---

## The Golden Rule

**Never use accuracy for imbalanced datasets.**

```
Fraud dataset: 9,990 legitimate, 10 fraud (0.1%)
Model always predicts "not fraud"
Accuracy = 9,990 / 10,000 = 99.9% ← Looks perfect. Catches ZERO fraud.
```

---

## Classification Metrics

### The Confusion Matrix

```
                Predicted: NOT FRAUD    Predicted: FRAUD
Actual: NOT FRAUD   True Negative (TN)    False Positive (FP) ← False alarm
Actual: FRAUD       False Negative (FN)   True Positive (TP)  ← Caught fraud
                    ↑ Missed fraud
```

### Precision vs Recall Trade-off

| Metric | Formula | Question | Low value means... |
|---|---|---|---|
| Precision | TP / (TP + FP) | When we say FRAUD, are we right? | Too many false alarms |
| Recall | TP / (TP + FN) | Do we catch all actual fraud? | Missing real fraud |
| F1 | 2×(P×R)/(P+R) | Balanced view of both | Both P and R bad |
| ROC-AUC | Area under ROC | Fundamental discrimination ability | Poor ranking |
| PR-AUC | Area under PR curve | Same but for imbalanced data | Use over ROC-AUC when imbalanced |

### Choosing Between Precision and Recall

| Scenario | Prioritize | Why |
|---|---|---|
| Medical screening | **Recall** | Missing disease is dangerous |
| Spam filter | **Precision** | Blocking real email is worse |
| Fraud (bank liability) | **Recall** | Missing fraud costs money |
| Fraud (customer experience) | **Precision** | Blocking legit customers is bad |

---

## Regression Metrics

| Metric | Formula | Outlier Sensitivity | Use When |
|---|---|---|---|
| MAE | avg(|actual - pred|) | Low | All errors equally bad |
| RMSE | √avg((actual-pred)²) | High | Large errors are especially costly |
| MAPE | avg(|actual-pred|/actual)% | Very High | Need scale-independent comparison |
| R² | 1 - SS_res/SS_tot | Medium | Comparing models on same dataset |

---

## Metric Selection Framework

```
Output type?
├── Binary (yes/no)
│   ├── Imbalanced? → PR-AUC + F-beta
│   └── Balanced?   → ROC-AUC + F1
├── Multi-class     → Per-class F1 + macro/weighted average
├── Number          → RMSE (large errors costly) or MAE (equal cost)
└── Ranking         → NDCG@K (full list) or MRR (first result)
```

---

## Calibration -- Are Probabilities Trustworthy?

A model says 70% fraud probability. Does fraud actually happen 70% of the time for those predictions?

```python
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

# Plot reliability diagram
prob_true, prob_pred = calibration_curve(y_test, y_scores, n_bins=10)

# Perfect calibration = diagonal line
# Points above = underconfident
# Points below = overconfident

# Fix with Platt scaling:
from sklearn.calibration import CalibratedClassifierCV
calibrated = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)
calibrated.fit(X_val, y_val)
```

---

**Next:** [04 -- Data Fundamentals →](04-data-fundamentals.md)
""")

write("ml-fundamentals/04-data-fundamentals.md", """
# 04 -- Data Fundamentals

> 80% of production ML failures originate in the data pipeline. Leakage, bad splits, imbalance, and training-serving skew cause more incidents than any model bug.

---

## Data Leakage -- The Silent Killer

Model has access to information during training that won't exist at prediction time.

| Type | Example | Detection |
|---|---|---|
| Future information | Using `loan_outcome` to predict loan default | Impossibly good metrics (99%+) |
| Target in features | Using `fraud_confirmed` to predict fraud | Near-perfect accuracy |
| Preprocessing leakage | Normalizing on full dataset before split | Works in dev, fails in prod |
| Group leakage | Same patient in both train and test | Good on test, bad on new entities |

```python
# WRONG: preprocessing leakage
X_scaled = scaler.fit_transform(X)  # uses test data!
X_train, X_test = train_test_split(X_scaled)

# RIGHT: fit only on training data
X_train, X_test = train_test_split(X)
X_train_scaled = scaler.fit_transform(X_train)   # learn from train only
X_test_scaled  = scaler.transform(X_test)          # apply to test
```

---

## Train / Validation / Test Split

```
Your dataset:
├── Training (70%)    → Model learns from this
├── Validation (15%)  → Tune hyperparameters, early stopping
└── Test (15%)        → Touch ONCE at the very end. Sacred. Never again.
```

**For time-series: NEVER shuffle randomly.**

```python
# WRONG: future data leaks into training
train, test = train_test_split(time_series_df, shuffle=True)

# RIGHT: chronological split
df = df.sort_values('timestamp')
split = int(len(df) * 0.8)
train = df.iloc[:split]   # past
test  = df.iloc[split:]   # future → realistic evaluation
```

---

## Handling Class Imbalance

```python
# Option 1: Class weighting (simplest)
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier()
model.fit(X_train, y_train, sample_weight=compute_sample_weight('balanced', y_train))

# Option 2: SMOTE (only on training data!)
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
# NEVER apply SMOTE to validation or test set

# Option 3: Threshold tuning
from sklearn.metrics import precision_recall_curve
precision, recall, thresholds = precision_recall_curve(y_val, y_proba)
f1_scores = 2 * precision * recall / (precision + recall + 1e-8)
best_threshold = thresholds[f1_scores.argmax()]
```

---

## Feature Engineering Essentials

```python
# Numerical: standardization (always on training data only)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)    # same params, don't refit
joblib.dump(scaler, 'artifacts/scaler.joblib')  # save for serving!

# Log transform for skewed features (e.g. transaction amounts)
df['amount_log'] = np.log1p(df['amount'])    # log(1+x), handles zeros

# Categorical: one-hot for low cardinality (<50 unique values)
df = pd.get_dummies(df, columns=['merchant_category'])

# Missing values: save imputer for serving
imputer = SimpleImputer(strategy='median')
imputer.fit(X_train)
joblib.dump(imputer, 'artifacts/imputer.joblib')  # must match serving!
```

---

## Training-Serving Skew Prevention

```python
# Always normalize timestamps to UTC before computing time features
df['timestamp_utc'] = pd.to_datetime(df['timestamp'], utc=True)
df['hour_utc'] = df['timestamp_utc'].dt.hour   # consistent in training AND serving

# Package preprocessing WITH the model
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('model', GradientBoostingClassifier())
])
pipeline.fit(X_train, y_train)
# Saving pipeline includes ALL preprocessing params -- no skew possible
joblib.dump(pipeline, 'artifacts/full_pipeline.joblib')
```

---

**Next:** [Core MLOps → Experiment Tracking](../core-mlops/01-experiment-tracking.md)
""")

# ─────────────────────────────────────────────────────────────────────────────
# PRODUCTION ENGINEERING (missing files)
# ─────────────────────────────────────────────────────────────────────────────
write("production-engineering/02-continuous-training.md", """
# 02 -- Continuous Training (CT) Pipelines

> Continuous Training is ML's equivalent of Continuous Deployment. Models must auto-retrain when the world changes, pass quality gates, and deploy safely.

---

## The 3 Retraining Triggers

| Trigger | How it Works | Best For |
|---|---|---|
| **Time-based** | Retrain every N days regardless | Simple, predictable, weakest |
| **Performance-based** | Retrain when accuracy drops below threshold | Gold standard, needs labels |
| **Drift-based** | Retrain when PSI > 0.2 on key features | Proactive, acts before degradation |

---

## The 7-Step CT Pipeline

```
[1] Data Validation      → Great Expectations checks. Abort if data is bad.
         ↓
[2] Feature Engineering  → Use same definitions as serving (feature store)
         ↓
[3] Model Training       → All params, seeds, data version logged to MLflow
         ↓
[4] Evaluation Gate      → Challenger must beat champion -- block if not
         ↓
[5] Model Registration   → Push to MLflow registry as "Staging"
         ↓
[6] Deployment           → Auto (low risk) or manual approval (high risk)
         ↓
[7] Post-Deploy Watch    → Monitor 24-72h → auto-rollback if degraded
```

---

## Prefect CT Pipeline

```python
from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
import mlflow
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

@task
def check_drift_trigger() -> bool:
    reference = load_training_reference()
    production = get_recent_predictions(days=7)
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=production)
    result = report.as_dict()
    psi = result["metrics"][0]["result"]["drift_share"]
    return psi > 0.10

@task
def validate_data(data_path: str) -> bool:
    df = pd.read_parquet(data_path)
    assert df["user_id"].notna().all(),   "Null user_ids found"
    assert (df["amount"] > 0).all(),       "Non-positive amounts found"
    assert df["transaction_id"].nunique() == len(df), "Duplicates found"
    return True

@task
def train_model(data_path: str) -> str:
    df = pd.read_parquet(data_path)
    X_train, X_val, y_train, y_val = prepare_splits(df)
    with mlflow.start_run() as run:
        mlflow.log_params({"data_version": get_dvc_hash(data_path), "git_commit": get_git_hash()})
        model = train(X_train, y_train)
        val_auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
        mlflow.log_metric("val_auc", val_auc)
        mlflow.sklearn.log_model(model, "model", registered_model_name="fraud_detector")
        return run.info.run_id

@task
def evaluate_gate(run_id: str) -> bool:
    challenger = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
    champion   = mlflow.sklearn.load_model("models:/fraud_detector/Production")
    X_test, y_test = load_holdout_test()
    challenger_auc = roc_auc_score(y_test, challenger.predict_proba(X_test)[:, 1])
    champion_auc   = roc_auc_score(y_test, champion.predict_proba(X_test)[:, 1])
    print(f"Champion: {champion_auc:.4f} | Challenger: {challenger_auc:.4f}")
    if challenger_auc < champion_auc - 0.005:
        raise ValueError(f"Challenger worse than champion -- blocking deployment")
    return True

@task
def promote_model(run_id: str):
    client = mlflow.tracking.MlflowClient()
    model_version = get_latest_version("fraud_detector")
    client.transition_model_version_stage(
        name="fraud_detector", version=model_version, stage="Production",
        archive_existing_versions=True
    )
    notify_slack(f"Fraud model v{model_version} promoted to production")

@flow(task_runner=SequentialTaskRunner())
def ct_pipeline():
    should_retrain = check_drift_trigger()
    if not should_retrain:
        print("No drift detected -- skipping retraining")
        return
    validate_data("data/training_latest.parquet")
    run_id = train_model("data/training_latest.parquet")
    gate_passed = evaluate_gate(run_id)
    if gate_passed:
        promote_model(run_id)

if __name__ == "__main__":
    ct_pipeline()
```

---

## Deployment Schedule

```yaml
# Kubernetes CronJob: run CT pipeline weekly
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ct-pipeline
spec:
  schedule: "0 2 * * 1"  # Monday 2am
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: ct-runner
              image: ml-training:latest
              command: ["python", "ct_pipeline.py"]
          restartPolicy: OnFailure
```

---

## Ground Truth Feedback Loop

The hardest part of CT: getting labels back into your system.

| Domain | How Labels Arrive | Label Latency |
|---|---|---|
| Fraud detection | Chargeback/dispute | 7-30 days |
| Medical diagnosis | Treatment outcome | Months |
| Content moderation | User reports | Hours-days |
| Click prediction | Click/no-click | Minutes |

**Design the feedback loop into your system from day one.** Retrain frequency is bounded by label latency.

---

**Next:** [03 -- Safe Deployments →](03-safe-deployments.md)
""")

write("production-engineering/04-drift-detection.md", """
# 04 -- Drift Detection

> Models don't crash when the world changes. They silently give worse answers. Drift monitoring is your early warning system.

---

## The 3 Types of Drift

| Type | What Changes | Example | Response |
|---|---|---|---|
| **Data drift** (Covariate shift) | Input distribution P(X) | New user demographic joins | Retrain with representative data |
| **Concept drift** | Relationship P(Y|X) | Fraud patterns fundamentally change | Rethink features, retraining strategy |
| **Label drift** | Target distribution P(Y) | Fraud rate drops from 1% to 0.01% | Adjust class weights, retune threshold |

**Critical:** These require completely different responses. Never treat concept drift as data drift.

---

## PSI -- Population Stability Index

Industry-standard metric for detecting input feature drift.

```python
import numpy as np

def compute_psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts   = np.histogram(actual,   bins=breakpoints)[0]

    expected_pct = np.where(expected_counts == 0, 0.0001, expected_counts / len(expected))
    actual_pct   = np.where(actual_counts   == 0, 0.0001, actual_counts   / len(actual))

    return float(np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct)))

# Thresholds:
# PSI < 0.10  → No significant drift
# PSI < 0.20  → Moderate drift -- monitor closely
# PSI >= 0.20 → Significant drift -- trigger retraining
```

---

## Evidently AI -- Complete Drift Dashboard

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import ColumnDriftMetric, ColumnDistributionMetric

def run_drift_report(reference_df, production_df, output_path="reports/drift.html"):
    report = Report(metrics=[
        DataDriftPreset(),
        DataQualityPreset(),
        ColumnDriftMetric(column_name="transaction_amount"),
        ColumnDriftMetric(column_name="fraud_probability"),  # monitor prediction dist
        ColumnDistributionMetric(column_name="fraud_probability"),
    ])
    report.run(reference_data=reference_df, current_data=production_df)
    report.save_html(output_path)

    result = report.as_dict()
    drift_detected = result["metrics"][0]["result"]["dataset_drift"]
    n_drifted = result["metrics"][0]["result"]["number_of_drifted_columns"]

    if drift_detected:
        trigger_retraining_alert(f"{n_drifted} features drifted -- check {output_path}")

    return result
```

---

## SHAP-Based Drift -- Early Warning

Track SHAP value distributions over time. If a feature's SHAP values shift, that feature is increasingly (or decreasingly) driving predictions -- a more sensitive signal than raw PSI.

```python
import shap
import numpy as np

def monitor_shap_drift(model, X_production, baseline_shap, feature_names):
    explainer = shap.TreeExplainer(model)
    production_shap = explainer.shap_values(X_production)

    baseline_importance   = np.abs(baseline_shap).mean(axis=0)
    production_importance = np.abs(production_shap).mean(axis=0)

    for i, feature in enumerate(feature_names):
        if baseline_importance[i] == 0:
            continue
        relative_change = abs(production_importance[i] - baseline_importance[i]) / baseline_importance[i]
        if relative_change > 0.30:  # >30% change in feature importance
            print(f"SHAP drift on '{feature}': {relative_change:.1%} change in importance")
```

---

## Prediction Distribution Monitoring

The fastest drift signal -- watch for shifts in your model's output distribution.

```python
def monitor_prediction_distribution(current_predictions, baseline_stats):
    current_mean = np.mean(current_predictions)
    current_std  = np.std(current_predictions)

    baseline_mean = baseline_stats["mean"]
    baseline_std  = baseline_stats["std"]

    # Mean shift
    if abs(current_mean - baseline_mean) > 2 * baseline_std:
        alert(f"Prediction mean shifted: {baseline_mean:.3f} → {current_mean:.3f}")

    # Distribution shape change (use KS test)
    from scipy.stats import ks_2samp
    ks_stat, p_value = ks_2samp(baseline_predictions, current_predictions)
    if p_value < 0.01:
        alert(f"Prediction distribution changed significantly (KS p={p_value:.4f})")
```

---

## Drift Response Runbook

```
PSI 0.10-0.20 on any feature:
    → Log and alert team
    → Increase monitoring frequency
    → No automatic retraining yet

PSI > 0.20 on any top-5 feature:
    → Trigger CT pipeline immediately
    → Send Slack alert with PSI scores
    → Begin root cause investigation

PSI > 0.20 on multiple features simultaneously:
    → This may be concept drift, not data drift
    → Do NOT just retrain -- investigate WHY features changed
    → May need new features or new model architecture

Prediction distribution shifts suddenly:
    → Check feature pipeline first (most likely cause)
    → Check if wrong model version was deployed
    → Check for upstream data schema changes
```

---

**Next:** [05 -- Model Explainability →](05-model-explainability.md)
""")

write("production-engineering/05-model-explainability.md", """
# 05 -- Model Explainability (SHAP + LIME)

> Explainability is not optional in regulated industries. It's also your best debugging tool for model behavior in production.

---

## Why Explainability Matters in Production

1. **Regulatory compliance** -- GDPR Article 22, EU AI Act, financial regulations require explanations for automated decisions
2. **Debugging** -- When a model makes a surprising prediction, SHAP tells you exactly why
3. **Drift detection** -- Tracking SHAP distributions over time reveals what's changing
4. **Trust** -- Business stakeholders and auditors need to understand what the model is doing

---

## SHAP -- The Gold Standard

SHAP (SHapley Additive exPlanations) answers: **"For this specific prediction, how much did each feature contribute?"**

```python
import shap
import numpy as np

model = load_model("models/fraud_detector.pkl")
X_test = load_test_data()

# TreeExplainer -- for tree models (XGBoost, LightGBM, Random Forest)
# Fast and exact -- use this in production
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
# shap_values shape: (n_samples, n_features)
# Each value: how much that feature pushed the prediction up or down
```

### Local Explanation (One Prediction)

```python
# Explain a single suspicious transaction
sample = X_test.iloc[42:43]
shap_val = explainer.shap_values(sample)[0]

print(f"Base rate (avg fraud probability): {explainer.expected_value:.3f}")
print(f"Final prediction: {model.predict_proba(sample)[0,1]:.3f}")
print()
for feat, sv in zip(feature_names, shap_val):
    direction = "▲" if sv > 0 else "▼"
    print(f"{direction} {feat:30s}: {sv:+.4f}")

# Output:
# Base rate: 0.082
# Final prediction: 0.891
# ▲ amount                        : +0.312  ← high amount pushed fraud prob up
# ▲ is_foreign                    : +0.245  ← foreign transaction adds risk
# ▲ hour_of_day (3am)             : +0.189  ← unusual time
# ▼ account_age_days              : -0.021  ← long-standing account reduces risk
```

### Global Explanation (All Predictions)

```python
# Which features matter most overall?
mean_abs_shap = np.abs(shap_values).mean(axis=0)
feature_importance = dict(zip(feature_names, mean_abs_shap))
sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)

print("Global Feature Importance (mean |SHAP|):")
for feat, importance in sorted_features[:10]:
    bar = "█" * int(importance * 100)
    print(f"{feat:30s} {importance:.4f} {bar}")
```

### SHAP in API Response

```python
@app.post("/predict")
async def predict(request: PredictionRequest):
    features = prepare_features(request)
    prediction = model.predict_proba(features)[0, 1]

    # Include explanation in response (for compliance)
    shap_values = explainer.shap_values(features)[0]
    explanation = {
        feat: round(float(sv), 4)
        for feat, sv in zip(feature_names, shap_values)
        if abs(sv) > 0.01  # only show significant contributors
    }

    return {
        "fraud_probability": round(float(prediction), 4),
        "explanation": explanation,
        "base_rate": round(float(explainer.expected_value), 4)
    }
```

---

## SHAP Explainer Types

| Explainer | Models | Speed | Accuracy |
|---|---|---|---|
| `TreeExplainer` | XGBoost, LightGBM, Random Forest | Fast | Exact |
| `LinearExplainer` | Linear/Logistic Regression | Fast | Exact |
| `DeepExplainer` | Neural Networks (PyTorch/TF) | Medium | Approximate |
| `KernelExplainer` | Any model | Very slow | Approximate |

**Rule:** Use `TreeExplainer` for tree models. Use `KernelExplainer` only as last resort.

---

## LIME -- When to Use Instead

LIME (Local Interpretable Model-agnostic Explanations) creates a local linear approximation around one prediction.

```python
from lime.lime_tabular import LimeTabularExplainer

explainer = LimeTabularExplainer(
    X_train.values,
    feature_names=feature_names,
    class_names=["legitimate", "fraud"],
    mode="classification"
)

explanation = explainer.explain_instance(
    X_test.iloc[42].values,
    model.predict_proba,
    num_features=10
)

# Get feature weights
for feat, weight in explanation.as_list():
    print(f"{feat}: {weight:+.4f}")
```

### SHAP vs LIME

| Factor | SHAP | LIME |
|---|---|---|
| Accuracy | Exact (tree models) | Approximate |
| Consistency | Same result every run | Non-deterministic |
| Speed | Fast for trees | Always slow |
| Best for | Production, compliance | Research, images, text |

**Use SHAP in production. Use LIME for exploration or non-tree models where SHAP is slow.**

---

**Next:** [06 -- Inference Patterns →](06-inference-patterns.md)
""")

write("production-engineering/06-inference-patterns.md", """
# 06 -- Batch vs Real-Time Inference Patterns

> Choosing the wrong inference pattern makes your system either too slow, too expensive, or both.

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

**Advantages:** Cheap, simple, no serving infrastructure, can use powerful hardware.

**Disadvantages:** Predictions are stale -- can't react to what user did in the last 5 minutes.

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

**Advantages:** Fresh predictions, highly personalized, reacts to current context.

**Disadvantages:** Expensive (model runs 24/7), latency pressure, complex infrastructure.

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
""")

# ─────────────────────────────────────────────────────────────────────────────
# ADVANCED SPECIALIZED
# ─────────────────────────────────────────────────────────────────────────────
write("advanced-specialized/01-distributed-training.md", """
# 01 -- Distributed Training (Ray + DeepSpeed)

> When a model doesn't fit on one GPU or training takes too long on one machine, distributed training is the solution.

---

## The 3 Walls You Hit

| Wall | Problem | Solution |
|---|---|---|
| **Memory** | Model doesn't fit in GPU VRAM (7B model = 28GB in FP32) | Model parallelism, ZeRO |
| **Time** | Training takes 3 weeks on one GPU | Data parallelism |
| **Data** | 50TB dataset can't load through one I/O | Distributed data loading |

---

## Data Parallelism -- Most Common

Copy the full model to every GPU. Split data across GPUs. Average gradients.

```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def train_ddp(rank, world_size):
    # Setup
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

    # Each GPU gets its own model copy
    model = FraudDetector().to(rank)
    model = DDP(model, device_ids=[rank])  # wraps with gradient sync

    # Each GPU gets a different data shard
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    loader = DataLoader(dataset, sampler=sampler, batch_size=64)

    optimizer = torch.optim.Adam(model.parameters())

    for batch in loader:
        optimizer.zero_grad()
        loss = criterion(model(batch["features"]), batch["labels"])
        loss.backward()           # gradients computed locally
        optimizer.step()          # DDP automatically averages gradients across GPUs

    dist.destroy_process_group()

# Launch on 4 GPUs
torch.multiprocessing.spawn(train_ddp, args=(4,), nprocs=4)
```

---

## ZeRO -- Memory Optimization (DeepSpeed)

Standard data parallelism: every GPU holds full model + gradients + optimizer states = 3× redundancy.

ZeRO eliminates redundancy by sharding across GPUs:

| Stage | Shards | Memory Reduction |
|---|---|---|
| ZeRO-1 | Optimizer states | 4× |
| ZeRO-2 | Optimizer states + Gradients | 8× |
| ZeRO-3 | Optimizer + Gradients + Parameters | ∝ number of GPUs |

```python
# deepspeed_config.json
{
    "zero_optimization": {
        "stage": 3,
        "offload_optimizer": {"device": "cpu"},  # offload to CPU RAM if needed
        "offload_param": {"device": "cpu"}
    },
    "fp16": {"enabled": true},
    "train_batch_size": 256
}
```

```bash
# Launch DeepSpeed training
deepspeed --num_gpus=8 train.py --deepspeed deepspeed_config.json
```

---

## Ray Train -- Distributed Training Made Simple

```python
import ray
from ray import train
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig

def train_func():
    model = FraudDetector()
    model = train.torch.prepare_model(model)       # DDP wrapper
    loader = train.torch.prepare_data_loader(loader)  # distributed sampler

    for epoch in range(10):
        for batch in loader:
            loss = compute_loss(model, batch)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        train.report({"loss": float(loss), "epoch": epoch})

trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(num_workers=4, use_gpu=True)
)
result = trainer.fit()
```

---

## Ray Tune -- Distributed Hyperparameter Search

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler

def train_with_params(config):
    model = GradientBoostingClassifier(
        n_estimators=config["n_estimators"],
        max_depth=config["max_depth"],
        learning_rate=config["learning_rate"]
    )
    model.fit(X_train, y_train)
    auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
    tune.report(val_auc=auc)

results = tune.run(
    train_with_params,
    config={
        "n_estimators": tune.randint(100, 1000),
        "max_depth": tune.randint(3, 10),
        "learning_rate": tune.loguniform(0.001, 0.3)
    },
    num_samples=50,                            # try 50 configurations
    scheduler=ASHAScheduler(metric="val_auc", mode="max"),  # kill bad trials early
    resources_per_trial={"cpu": 4}
)
print(results.best_config)
```

---

**Next:** [02 -- Kubernetes-Native ML →](02-kubernetes-native-ml.md)
""")

write("advanced-specialized/02-kubernetes-native-ml.md", """
# 02 -- Kubernetes-Native ML (KFP + Argo)

> In Kubernetes-native ML, every pipeline step runs in its own isolated container with its own resource allocation. This is enterprise-grade ML infrastructure.

---

## Why Not Just Use Airflow for ML?

| Airflow | Kubernetes-Native (KFP/Argo) |
|---|---|
| All tasks share same Python environment | Every step in its own container |
| All tasks share same compute resources | Each step gets exactly the resources it needs |
| Training step can't request 8 GPUs easily | Training step requests `nvidia.com/gpu: 8` |
| One failure can affect other running tasks | Complete isolation -- failures don't spread |
| Limited caching | Built-in step caching (skip unchanged steps) |

---

## KubeFlow Pipelines (KFP) -- Complete Example

```python
from kfp import dsl
from kfp.dsl import component, pipeline, Input, Output, Dataset, Model, Metrics

# Each @component runs in its own container
@component(
    base_image="python:3.10",
    packages_to_install=["pandas", "great-expectations", "pyarrow"]
)
def validate_data(
    data_path: str,
    validated_data: Output[Dataset]
):
    import pandas as pd
    df = pd.read_parquet(data_path)
    assert df["user_id"].notna().all(), "Null user_ids"
    assert (df["amount"] > 0).all(), "Non-positive amounts"
    df.to_parquet(validated_data.path)
    print(f"Validated {len(df):,} rows")

@component(
    base_image="nvcr.io/nvidia/pytorch:23.10-py3",  # GPU image for training
    packages_to_install=["mlflow", "scikit-learn", "xgboost"]
)
def train_model(
    training_data: Input[Dataset],
    model_artifact: Output[Model],
    metrics: Output[Metrics],
    n_estimators: int = 300,
    max_depth: int = 6
):
    import mlflow
    from sklearn.metrics import roc_auc_score
    import pandas as pd, joblib

    df = pd.read_parquet(training_data.path)
    X, y = df.drop("is_fraud", axis=1), df["is_fraud"]

    with mlflow.start_run():
        from xgboost import XGBClassifier
        model = XGBClassifier(n_estimators=n_estimators, max_depth=max_depth)
        model.fit(X, y)
        val_auc = roc_auc_score(y, model.predict_proba(X)[:, 1])
        mlflow.log_metric("val_auc", val_auc)

    joblib.dump(model, model_artifact.path)
    metrics.log_metric("val_auc", val_auc)

@component(base_image="python:3.10", packages_to_install=["scikit-learn", "mlflow"])
def evaluate_gate(
    model: Input[Model],
    metrics: Input[Metrics],
    champion_model_uri: str
) -> bool:
    import mlflow, joblib
    from sklearn.metrics import roc_auc_score

    challenger = joblib.load(model.path)
    champion   = mlflow.sklearn.load_model(champion_model_uri)
    X_test, y_test = load_holdout_test()

    challenger_auc = roc_auc_score(y_test, challenger.predict_proba(X_test)[:, 1])
    champion_auc   = roc_auc_score(y_test, champion.predict_proba(X_test)[:, 1])

    print(f"Challenger: {challenger_auc:.4f} | Champion: {champion_auc:.4f}")
    return challenger_auc >= champion_auc - 0.005

@pipeline(name="fraud-detection-training", description="Weekly CT pipeline")
def fraud_training_pipeline(data_path: str = "s3://data/training_latest.parquet"):
    # Step 1: runs in 2-CPU, 4GB pod
    validate_task = validate_data(data_path=data_path)

    # Step 2: runs in GPU pod (4x A100)
    train_task = train_model(
        training_data=validate_task.outputs["validated_data"],
        n_estimators=300, max_depth=6
    ).set_accelerator_type("NVIDIA_TESLA_A100").set_accelerator_limit(4)

    # Step 3: runs in 2-CPU pod
    gate_task = evaluate_gate(
        model=train_task.outputs["model_artifact"],
        metrics=train_task.outputs["metrics"],
        champion_model_uri="models:/fraud_detector/Production"
    ).after(train_task)

if __name__ == "__main__":
    from kfp import compiler
    compiler.Compiler().compile(fraud_training_pipeline, "pipeline.yaml")
    # Submit: kfp.Client().create_run_from_pipeline_func(fraud_training_pipeline, arguments={})
```

---

## Argo Workflows -- Container-First Alternative

```yaml
# fraud-training-workflow.yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: fraud-training
spec:
  entrypoint: training-dag

  templates:
    - name: training-dag
      dag:
        tasks:
          - name: validate-data
            template: validate
          - name: train-model
            template: train
            dependencies: [validate-data]
            arguments:
              artifacts:
                - name: training-data
                  from: "{{tasks.validate-data.outputs.artifacts.validated-data}}"
          - name: evaluate-gate
            template: evaluate
            dependencies: [train-model]

    - name: validate
      container:
        image: data-validator:latest
        command: [python, validate.py]
        resources:
          requests: {memory: "4Gi", cpu: "2"}

    - name: train
      inputs:
        artifacts:
          - name: training-data
            path: /data/train.parquet
      container:
        image: ml-trainer:latest
        command: [python, train.py, --data, /data/train.parquet]
        resources:
          requests: {memory: "64Gi", cpu: "16"}
          limits:
            nvidia.com/gpu: "4"

    - name: evaluate
      container:
        image: ml-evaluator:latest
        command: [python, evaluate.py]
        resources:
          requests: {memory: "8Gi", cpu: "4"}
```

---

**Next:** [03 -- Model Compression →](03-model-compression.md)
""")

write("advanced-specialized/03-model-compression.md", """
# 03 -- Model Compression & Optimization

> A model optimized 3× costs 66% less to serve. For a $10,000/month endpoint, one week of compression work saves $79,920/year.

---

## Quantization -- Reduce Numerical Precision

Weights stored as FP32 (4 bytes) → INT8 (1 byte) = 4× smaller, 4× faster on supported hardware.

| Precision | Bytes/Parameter | 7B Model | Quality Loss |
|---|---|---|---|
| FP32 | 4 | 28 GB | None (baseline) |
| FP16 / BF16 | 2 | 14 GB | Minimal |
| INT8 | 1 | 7 GB | Small |
| INT4 / NF4 | 0.5 | 3.5 GB | Moderate |

### Post-Training Quantization (PTQ) -- No Retraining

```python
from transformers import AutoModelForSequenceClassification
from optimum.onnxruntime import ORTModelForSequenceClassification
from optimum.onnxruntime.configuration import AutoQuantizationConfig

# Load and quantize in one step
quantization_config = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False)

quantizer = ORTQuantizer.from_pretrained("bert-base-uncased-finetuned-fraud")
quantizer.quantize(
    save_dir="bert-fraud-int8",
    quantization_config=quantization_config
)

# Load quantized model for serving -- 4× smaller, 3× faster
model = ORTModelForSequenceClassification.from_pretrained("bert-fraud-int8")
```

### Quantization-Aware Training (QAT) -- Retrain for Better Quality

```python
import torch
from torch.quantization import prepare_qat, convert

model = FraudDetector()

# Simulate quantization during training -- model learns to be robust to it
model.train()
model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
model_prepared = prepare_qat(model)

# Train normally -- quantization simulation is automatic
for epoch in range(10):
    for batch in train_loader:
        loss = criterion(model_prepared(batch["features"]), batch["labels"])
        loss.backward()
        optimizer.step()

# Convert to actual quantized model
model_prepared.eval()
model_int8 = convert(model_prepared)
torch.save(model_int8.state_dict(), "model_int8.pt")
```

---

## ONNX -- Universal Serving Format

Train in any framework. Serve with ONNX Runtime -- faster, no framework dependency.

```python
import torch

# Export PyTorch model to ONNX
model.eval()
dummy_input = torch.randn(1, 20)  # 20 input features

torch.onnx.export(
    model,
    dummy_input,
    "fraud_detector.onnx",
    input_names=["features"],
    output_names=["fraud_probability"],
    dynamic_axes={"features": {0: "batch_size"}, "fraud_probability": {0: "batch_size"}},
    opset_version=17
)

# Serve with ONNX Runtime -- no PyTorch needed at serving time
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession(
    "fraud_detector.onnx",
    providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
)

# Inference
features = np.array([[...]], dtype=np.float32)
result = session.run(["fraud_probability"], {"features": features})
probability = float(result[0][0])
```

---

## TensorRT -- Maximum GPU Performance

Convert ONNX to TensorRT for 3-10× speedup on NVIDIA GPUs.

```bash
# Convert ONNX to TensorRT engine
trtexec \
    --onnx=fraud_detector.onnx \
    --saveEngine=fraud_detector.trt \
    --fp16 \                          # use FP16 precision
    --minShapes=features:1x20 \       # minimum batch
    --optShapes=features:32x20 \      # optimal batch (tune this)
    --maxShapes=features:128x20       # maximum batch
```

```python
import tensorrt as trt
import numpy as np
import pycuda.driver as cuda

# Load TensorRT engine
with open("fraud_detector.trt", "rb") as f:
    engine = trt.Runtime(trt.Logger()).deserialize_cuda_engine(f.read())

context = engine.create_execution_context()
# ... inference code
```

---

## Knowledge Distillation

Train a small "student" model to mimic a large "teacher" model.

```python
import torch.nn.functional as F

teacher = load_large_model()  # 70B parameters -- accurate but slow
student = SmallModel()        # 7B parameters -- fast

teacher.eval()
for batch in train_loader:
    # Teacher's soft predictions -- contain richer information than hard labels
    with torch.no_grad():
        teacher_logits = teacher(batch["features"])

    # Student learns from teacher's soft probabilities (not just hard labels)
    student_logits = student(batch["features"])

    # Distillation loss: match teacher's probability distribution
    T = 4.0  # temperature -- higher = softer distributions
    distillation_loss = F.kl_div(
        F.log_softmax(student_logits / T, dim=1),
        F.softmax(teacher_logits / T, dim=1),
        reduction="batchmean"
    ) * (T ** 2)

    # Hard label loss: also learn from ground truth
    hard_loss = F.cross_entropy(student_logits, batch["labels"])

    # Combine: 70% distillation, 30% hard labels
    loss = 0.7 * distillation_loss + 0.3 * hard_loss
    loss.backward()
    optimizer.step()
```

---

## The Production Optimization Pipeline

```
1. Baseline: train model in PyTorch (FP32)
             measure: latency=200ms, memory=4GB, throughput=50 req/s

2. Export to ONNX
             measure: latency=80ms, memory=3.5GB, throughput=120 req/s

3. Quantize (INT8 PTQ)
             measure: latency=40ms, memory=1GB, throughput=280 req/s

4. Compile to TensorRT (FP16)
             measure: latency=20ms, memory=900MB, throughput=600 req/s

5. Add dynamic batching (Triton)
             measure: throughput=3,000+ req/s

Total improvement: 10× lower latency, 80% cost reduction
```

---

**Next:** [04 -- Multi-Model Serving (Triton) →](04-multi-model-serving.md)
""")

write("advanced-specialized/04-multi-model-serving.md", """
# 04 -- Multi-Model Serving (NVIDIA Triton)

> When you have 10+ models to serve, managing separate containers per model is an operational nightmare. Triton serves all models from a unified platform.

---

## Why Triton?

| Approach | Problem |
|---|---|
| One FastAPI container per model | 20 models = 20 deployments, 20 CI/CD pipelines, 20 monitoring setups |
| NVIDIA Triton Inference Server | One server hosts all models, all frameworks, managed automatically |

---

## Triton Model Repository

Drop model files in a directory structure. Triton auto-loads them.

```
model_repository/
├── fraud_detector/
│   ├── 1/                     ← version 1
│   │   └── model.onnx
│   ├── 2/                     ← version 2 (both served simultaneously!)
│   │   └── model.onnx
│   └── config.pbtxt           ← model configuration
│
├── sentiment_classifier/
│   ├── 1/
│   │   └── model.pt
│   └── config.pbtxt
│
└── fraud_ensemble/            ← pipeline: preprocessor → model → postprocessor
    ├── 1/
    └── config.pbtxt
```

---

## Model Configuration

```protobuf
# fraud_detector/config.pbtxt
name: "fraud_detector"
platform: "onnxruntime_onnx"
max_batch_size: 128

input [
  {
    name: "features"
    data_type: TYPE_FP32
    dims: [20]
  }
]

output [
  {
    name: "fraud_probability"
    data_type: TYPE_FP32
    dims: [1]
  }
]

# Dynamic batching: collect requests for up to 5ms, batch them together
dynamic_batching {
  preferred_batch_size: [8, 16, 32, 64]
  max_queue_delay_microseconds: 5000
}

# Load 2 instances simultaneously on the GPU
instance_group [
  { count: 2, kind: KIND_GPU }
]
```

---

## Dynamic Batching -- The Key Feature

GPU throughput increases dramatically with batch size. Dynamic batching automatically groups individual requests.

```
Without batching:
  Request 1 arrives → GPU inference (20ms) → response
  Request 2 arrives → GPU inference (20ms) → response
  Request 3 arrives → GPU inference (20ms) → response
  Total: 60ms for 3 requests, GPU utilization: 15%

With dynamic batching (5ms wait window):
  Requests 1, 2, 3 arrive within 5ms
  GPU inference on batch of 3 (22ms) → 3 responses
  Total: 27ms for 3 requests, GPU utilization: 80%+
  Throughput: 3× improvement
```

---

## Ensemble Pipelines

Chain multiple models into a single API call.

```protobuf
# fraud_ensemble/config.pbtxt
name: "fraud_ensemble"
platform: "ensemble"
max_batch_size: 128

ensemble_scheduling {
  step [
    {
      model_name: "feature_preprocessor"
      model_version: -1           # -1 = latest
      input_map { key: "raw_features", value: "RAW_INPUT" }
      output_map { key: "processed_features", value: "PROCESSED" }
    },
    {
      model_name: "fraud_detector"
      model_version: -1
      input_map { key: "features", value: "PROCESSED" }
      output_map { key: "fraud_probability", value: "FINAL_OUTPUT" }
    }
  ]
}
```

---

## Client Code

```python
import tritonclient.http as tritonhttp
import numpy as np

client = tritonhttp.InferenceServerClient("localhost:8000")

# Single model inference
features = np.array([[...]], dtype=np.float32)

inputs = [tritonhttp.InferInput("features", features.shape, "FP32")]
inputs[0].set_data_from_numpy(features)

outputs = [tritonhttp.InferRequestedOutput("fraud_probability")]

response = client.infer(
    model_name="fraud_detector",
    model_version="2",          # specific version
    inputs=inputs,
    outputs=outputs
)

probability = response.as_numpy("fraud_probability")[0]
print(f"Fraud probability: {probability:.4f}")
```

---

## Deploy Triton on Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: triton-serving
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: triton
          image: nvcr.io/nvidia/tritonserver:23.10-py3
          args:
            - tritonserver
            - --model-repository=s3://my-bucket/model_repository
            - --log-verbose=1
            - --metrics-port=8002
          ports:
            - containerPort: 8000   # HTTP
            - containerPort: 8001   # gRPC
            - containerPort: 8002   # Prometheus metrics
          resources:
            limits:
              nvidia.com/gpu: "1"
          readinessProbe:
            httpGet:
              path: /v2/health/ready
              port: 8000
            initialDelaySeconds: 60
```

---

**Next:** [05 -- ML Platform Design →](05-platform-design.md)
""")

write("advanced-specialized/05-platform-design.md", """
# 05 -- ML Platform Design Patterns

> An ML platform is the infrastructure, tooling, and workflows that let data scientists develop, train, deploy, and monitor models -- without managing infrastructure themselves.

---

## The 3 Maturity Levels

| Level | State | How Models Get Deployed |
|---|---|---|
| **Level 1** | Manual everything | Data scientist hands Jupyter notebook to engineer who manually deploys |
| **Level 2** | Automated pipelines | CI/CD exists, MLflow tracks experiments, deployments are scripted |
| **Level 3** | Self-service platform | Data scientist runs `platform.deploy(model)` and it's live in 10 minutes |

Most companies are at Level 1.5. Engineers who can move a company from L1 → L2 → L3 are among the most valuable in the org.

---

## Build vs Buy Decision

```
Build on Kubernetes + OSS when:
  ✓ 10+ ML engineers, dedicated platform team exists
  ✓ Data cannot leave on-prem (healthcare, finance, government)
  ✓ Need full customization (exotic hardware, unusual model types)
  ✓ At scale where cloud markup is prohibitive
  ✓ Multi-cloud or hybrid-cloud strategy

Buy managed platform (SageMaker / Vertex / Azure ML) when:
  ✓ Team < 10 ML engineers, moving fast
  ✓ No platform engineers available
  ✓ Already cloud-committed (all data in AWS/GCP/Azure)
  ✓ Standard use cases (classification, regression, standard NLP)

Hybrid (what most serious companies actually do):
  ✓ Use managed for commodity: storage, databases, networking
  ✓ Build for differentiating: custom serving, specialized monitoring
```

---

## Core Platform Design Principles

### 1. Separation of Concerns

```
Data     → object storage (S3, GCS, MinIO)  ← cheap, durable, scalable
Compute  → ephemeral (Kubernetes Jobs)       ← spin up, run, destroy
Metadata → relational database (PostgreSQL)  ← MLflow tracking, model registry
```

### 2. Everything as Code

```yaml
# ALL configuration in Git -- never in a UI only
training_config.yaml      → training parameters
serving_config.yaml        → deployment config
monitoring_thresholds.yaml → alert thresholds
feature_definitions.py     → Feast feature definitions
pipeline_definition.py     → KFP pipeline
```

### 3. The Golden Path

```python
# What data scientists should be able to write:
from ml_platform import Platform

platform = Platform()

# Submit training job (platform handles Kubernetes, GPUs, MLflow, etc.)
run = platform.submit_training(
    script="train.py",
    dataset="s3://data/fraud/v5",
    gpu_count=4,
    experiment="fraud-v2"
)

# Deploy to production (platform handles canary, monitoring, alerts)
platform.deploy(
    model_name="fraud_detector",
    run_id=run.id,
    traffic_strategy="canary",
    monitoring_config={"alert_on_drift": True}
)
```

### 4. Self-Service

```
Goal: New data scientist productive in 1 day, not 1 month.

Means:
  - Python SDK for everything
  - CLI for automation
  - UI for visibility
  - Documentation that's actually accurate
```

---

## The Metadata Store Pattern

Every artifact -- dataset, model, feature set, deployment -- generates metadata.

```python
# ML Metadata Store: full lineage tracking
class MLMetadata:
    def log_training_run(self, run_id, model_id, dataset_id, metrics):
        # Every training run: what code, what data, what model, what metrics
        pass

    def log_deployment(self, model_id, endpoint_id, traffic_pct):
        # Every deployment: which model, to where, serving what % of traffic
        pass

    def get_lineage(self, prediction_id):
        # For any prediction: what model, what training run, what data
        # Returns: prediction → model_v24 → run_abc123 → dataset_v5 → raw_data_jan_2024
        pass
```

This is required for:
- Compliance (GDPR, EU AI Act: "explain this automated decision")
- Debugging ("why did behavior change after last week's deployment?")
- Reproducibility ("reproduce the model from 6 months ago")

---

## FinMLOps -- Cost Discipline

```python
# Cost attribution: know who spends what
labels:
  team: "risk-ml"
  project: "fraud-detection"
  model: "fraud-detector-v24"
  environment: "production"

# MLflow: log cost per training run
with mlflow.start_run():
    start_time = time.time()
    train_model()
    duration_hours = (time.time() - start_time) / 3600
    
    instance_cost_per_hour = 3.20  # p3.2xlarge
    total_cost = duration_hours * instance_cost_per_hour
    mlflow.log_metric("training_cost_usd", total_cost)

# Cost optimization: spot instances for training
# Spot/preemptible instances: 60-80% cheaper than on-demand
# Requirement: checkpointing every N steps so training resumes after preemption
```

---

**Next:** [LLMOps →](../llmops/01-llmops-complete.md)
""")

# ─────────────────────────────────────────────────────────────────────────────
# PRACTICAL SKILLS
# ─────────────────────────────────────────────────────────────────────────────
write("practical-skills/01-docker-for-ml.md", """
# 01 -- Docker for ML

> ML workloads use Docker differently from standard software. GPU containers, CUDA compatibility, and multi-stage builds are ML-specific skills.

---

## GPU Containers -- The Key Difference

Regular Docker cannot access the host GPU. NVIDIA Container Toolkit bridges this.

```bash
# Install NVIDIA Container Toolkit (once on the host)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Test: access GPU inside container
docker run --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

---

## CUDA Version Compatibility

The most common ML Docker pain point.

```
GPU Driver Version  →  supports CUDA up to version X
CUDA Version        →  must match what PyTorch/TF was compiled for
PyTorch Version     →  compiled for specific CUDA version

If any mismatch → nothing works
```

```bash
# Check on host machine
nvidia-smi | grep "CUDA Version"   # max CUDA the driver supports

# Check inside container
python -c "import torch; print('PyTorch CUDA:', torch.version.cuda)"
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

**Use NVIDIA's pre-built base images -- never install CUDA manually:**

```dockerfile
# Training (full CUDA toolkit)
FROM nvcr.io/nvidia/pytorch:23.10-py3

# Serving (smaller -- runtime only, no compiler)
FROM nvcr.io/nvidia/cuda:12.2.0-runtime-ubuntu22.04
```

---

## Multi-Stage Build -- Keep Images Small

Without multi-stage builds, ML images easily reach 15GB.

```dockerfile
# Stage 1: Build environment (has all build tools)
FROM nvcr.io/nvidia/pytorch:23.10-py3 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (only what's needed to serve)
FROM nvcr.io/nvidia/cuda:12.2.0-runtime-ubuntu22.04

WORKDIR /app
# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local
COPY serve.py .
COPY model/ ./model/

# Non-root user (security)
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "serve.py"]
```

---

## Layer Caching Strategy

```dockerfile
# WRONG: one big layer -- any change rebuilds everything
RUN pip install torch transformers fastapi pydantic uvicorn

# RIGHT: separate stable and changing dependencies
# Stable (changes rarely) → cached
RUN pip install torch==2.1.0 transformers==4.35.0

# Changing (updates often) → layer below stable ones
COPY requirements-app.txt .
RUN pip install -r requirements-app.txt

# Code (changes most often) → last
COPY src/ ./src/
```

---

## Model Loading Strategies

```dockerfile
# Option A: Bake model into image (self-contained, large images)
COPY models/fraud_model_v23.onnx /app/model/

# Option B: Download at startup (small image, model from registry)
# In your serve.py:
import mlflow
model = mlflow.sklearn.load_model("models:/fraud_detector/Production")

# Option C: Mount as volume (fastest startup, needs infrastructure)
# docker run -v /host/models:/app/model fraud-serving:latest
```

---

## Essential .dockerignore

```dockerignore
# Large data files (tracked by DVC)
data/
*.csv
*.parquet
*.pkl

# Python
__pycache__/
*.pyc
.venv/
venv/
*.egg-info/

# Git
.git/
.gitignore

# IDE
.vscode/
.idea/

# Secrets (NEVER in Docker context)
.env
secrets.yaml
*.key
```

---

## Debugging Inside Containers

```bash
# Shell into a running container
docker exec -it <container_id> /bin/bash

# Check GPU inside container
docker exec -it <container_id> nvidia-smi

# Check PyTorch GPU access
docker exec -it <container_id> python -c "
import torch
print('GPUs:', torch.cuda.device_count())
print('GPU 0:', torch.cuda.get_device_name(0))
print('Memory allocated:', torch.cuda.memory_allocated() / 1e9, 'GB')
"

# Stream logs
docker logs -f <container_id>

# Resource usage
docker stats <container_id>
```

---

**Next:** [02 -- Kubernetes for ML →](02-kubernetes-for-ml.md)
""")

write("practical-skills/02-kubernetes-for-ml.md", """
# 02 -- Kubernetes for ML

> Your DevOps K8s knowledge applies directly. These are the ML-specific patterns on top.

---

## GPU Resource Requests

```yaml
resources:
  requests:
    memory: "16Gi"
    cpu: "4"
    nvidia.com/gpu: "1"    # request GPU
  limits:
    memory: "32Gi"
    cpu: "8"
    nvidia.com/gpu: "1"    # GPU limits must EQUAL requests (not greater)
```

**GPU limits must equal requests.** Unlike CPU (throttleable), GPU is binary -- you have it or you don't.

---

## Diagnosing Pod Failures

```bash
# Why is pod in CrashLoopBackOff?
kubectl logs <pod> --previous              # logs from crashed container

# GPU OOM looks like:
# RuntimeError: CUDA out of memory. Tried to allocate 2.50 GiB
# Fix: reduce batch size or use smaller model

# Container OOM looks like:
# Killed (exit code 137)
# Fix: increase memory limits

# Why is pod Pending (not scheduling)?
kubectl describe pod <pod>                 # read Events section at bottom
# "Insufficient nvidia.com/gpu" → no GPU nodes available
# "Insufficient memory" → all nodes too full

# Live resource usage
kubectl top pods --sort-by=memory
kubectl top nodes
```

---

## Persistent Volumes for Training

Training jobs must write checkpoints. If pod crashes, don't lose 8 hours of work.

```yaml
# Create PVC for training checkpoints
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: training-checkpoints
spec:
  accessModes:
    - ReadWriteOnce           # one pod reads/writes
  resources:
    requests:
      storage: 100Gi
  storageClassName: fast-ssd

# For distributed training (multiple pods need same data):
# accessModes: ReadWriteMany
# storageClassName: efs    # AWS EFS or NFS
```

```yaml
# Use in training pod
containers:
  - name: trainer
    volumeMounts:
      - mountPath: /checkpoints
        name: checkpoints
volumes:
  - name: checkpoints
    persistentVolumeClaim:
      claimName: training-checkpoints
```

---

## Kubernetes Jobs for Training

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: fraud-model-training-v25
spec:
  completions: 1
  backoffLimit: 3            # retry up to 3 times on failure
  template:
    spec:
      restartPolicy: OnFailure   # restart on failure, not on success
      containers:
        - name: trainer
          image: fraud-training:v25
          resources:
            limits:
              nvidia.com/gpu: "4"
              memory: "128Gi"
              cpu: "32"
          env:
            - name: MLFLOW_TRACKING_URI
              value: "http://mlflow-service:5000"
            - name: DATA_PATH
              value: "s3://data/fraud/training_v5.parquet"
          volumeMounts:
            - mountPath: /checkpoints
              name: checkpoints
      volumes:
        - name: checkpoints
          persistentVolumeClaim:
            claimName: training-checkpoints
```

---

## Init Containers -- Download Before Training

```yaml
initContainers:
  - name: download-data
    image: amazon/aws-cli:latest
    command:
      - aws
      - s3
      - sync
      - s3://my-bucket/training-data/v5/
      - /data/
    volumeMounts:
      - mountPath: /data
        name: training-data

containers:
  - name: trainer
    image: fraud-training:v25
    volumeMounts:
      - mountPath: /data
        name: training-data   # data is ready before trainer starts
```

---

## Readiness vs Liveness Probes for ML

```yaml
containers:
  - name: fraud-serving
    # readinessProbe: Kubernetes routes traffic ONLY when ready
    # Critical: large models take 30-120s to load
    readinessProbe:
      httpGet:
        path: /ready      # your endpoint checks if model is loaded
        port: 8000
      initialDelaySeconds: 60    # wait 60s before first check
      periodSeconds: 10

    # livenessProbe: restart pod if unhealthy
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 120
      periodSeconds: 30
```

---

## Useful Commands for ML Ops

```bash
# Shell into running serving pod (for debugging)
kubectl exec -it <pod> -- /bin/bash

# Check GPU memory in serving pod
kubectl exec <pod> -- python -c "
import torch
alloc = torch.cuda.memory_allocated() / 1e9
reserved = torch.cuda.memory_reserved() / 1e9
print(f'Allocated: {alloc:.2f}GB | Reserved: {reserved:.2f}GB')
"

# Scale serving deployment
kubectl scale deployment fraud-serving --replicas=5

# Watch rollout progress
kubectl rollout status deployment/fraud-serving

# Roll back if new version has problems
kubectl rollout undo deployment/fraud-serving

# Port-forward MLflow for local access
kubectl port-forward svc/mlflow-service 5000:5000
```

---

**Next:** [03 -- Testing ML Systems →](03-testing-ml-systems.md)
""")

write("practical-skills/03-testing-ml-systems.md", """
# 03 -- Testing ML Systems

> ML testing is fundamentally different from software testing. You test data quality, model behavior, pipeline correctness, and regression against production.

---

## The 4 Levels of ML Testing

```
Level 1: Data Tests          → validate data before model sees it
Level 2: Model Tests         → validate model behavior
Level 3: Pipeline Tests      → validate end-to-end workflows
Level 4: Regression Gate     → challenger must beat champion
```

---

## Level 1 -- Data Tests

```python
# tests/test_data.py
import pandas as pd
import numpy as np
import pytest

@pytest.fixture
def training_data():
    return pd.read_parquet("data/training_data.parquet")

def test_no_nulls_in_critical_columns(training_data):
    critical = ["user_id", "transaction_id", "amount", "is_fraud"]
    for col in critical:
        assert training_data[col].isnull().sum() == 0, f"Nulls found in {col}"

def test_amount_is_positive(training_data):
    assert (training_data["amount"] > 0).all(), "Non-positive amounts found"

def test_no_duplicate_transactions(training_data):
    dup_count = training_data["transaction_id"].duplicated().sum()
    assert dup_count == 0, f"Found {dup_count} duplicate transaction_ids"

def test_fraud_rate_is_reasonable(training_data):
    fraud_rate = training_data["is_fraud"].mean()
    assert 0.0005 < fraud_rate < 0.3, f"Unusual fraud rate: {fraud_rate:.4%}"

def test_no_future_dates(training_data):
    max_date = training_data["timestamp"].max()
    assert max_date <= pd.Timestamp.now(), f"Future dates found: {max_date}"

def test_minimum_training_samples(training_data):
    assert len(training_data) >= 10_000, f"Too few samples: {len(training_data)}"
```

---

## Level 2 -- Model Tests

```python
# tests/test_model.py
import numpy as np
import pytest
from src.model import load_model, create_test_input

@pytest.fixture
def model():
    return load_model("models/fraud_detector_latest.pkl")

def test_predictions_are_valid_probabilities(model):
    X = create_test_input(n_samples=1000)
    preds = model.predict_proba(X)[:, 1]
    assert preds.min() >= 0.0, "Negative probabilities!"
    assert preds.max() <= 1.0, "Probabilities > 1!"
    assert not np.isnan(preds).any(), "NaN predictions!"
    assert not np.isinf(preds).any(), "Infinite predictions!"

def test_model_is_deterministic(model):
    X = create_test_input(n_samples=10)
    pred1 = model.predict_proba(X)
    pred2 = model.predict_proba(X)
    np.testing.assert_array_almost_equal(pred1, pred2, decimal=6)

def test_model_handles_all_null_optional_fields(model):
    X = create_test_input_with_nulls()   # optional fields set to NaN
    preds = model.predict_proba(X)       # should not crash
    assert not np.isnan(preds).any()

def test_high_risk_scores_higher_than_low_risk(model):
    safe = create_input(amount=50, is_foreign=False, hour=14, credit_score=800)
    risky = create_input(amount=50000, is_foreign=True, hour=3, credit_score=400)
    safe_prob = model.predict_proba(safe)[0, 1]
    risky_prob = model.predict_proba(risky)[0, 1]
    assert risky_prob > safe_prob, (
        f"Model doesn't make sense: risky={risky_prob:.3f} < safe={safe_prob:.3f}"
    )

def test_model_prediction_speed(model):
    import time
    X = create_test_input(n_samples=100)
    start = time.time()
    model.predict_proba(X)
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 100, f"Batch of 100 took {elapsed_ms:.0f}ms (limit: 100ms)"
```

---

## Level 3 -- Pipeline Tests

```python
# tests/test_pipeline.py
import pytest
from src.pipeline import run_training_pipeline

def test_training_pipeline_runs_end_to_end(tmp_path):
    # Test full pipeline on tiny dataset -- should complete without errors.
    # Create minimal test data
    create_test_dataset(n_rows=500, output_path=tmp_path / "test_data.parquet")

    result = run_training_pipeline(
        data_path=str(tmp_path / "test_data.parquet"),
        output_path=str(tmp_path / "model"),
        max_epochs=2,           # don't need full training
        experiment_name="test"  # use test experiment
    )

    assert result.status == "SUCCESS"
    assert (tmp_path / "model").exists()
    assert result.mlflow_run_id is not None

def test_serving_api_validates_input():
    from fastapi.testclient import TestClient
    from src.serve import app

    client = TestClient(app)

    # Missing required field
    response = client.post("/predict", json={"user_id": "u1"})
    assert response.status_code == 422    # validation error, not 500

    # Wrong type
    response = client.post("/predict", json={"user_id": "u1", "amount": "not_a_number"})
    assert response.status_code == 422

    # Valid request
    valid = {"user_id": "u1", "amount": 150.0, "is_foreign": False, "hour_of_day": 14}
    response = client.post("/predict", json=valid)
    assert response.status_code == 200
    data = response.json()
    assert "fraud_probability" in data
    assert 0 <= data["fraud_probability"] <= 1
```

---

## Level 4 -- Deployment Gate (Most Important)

```python
# tests/test_deployment_gate.py -- runs in CI before every deployment
import mlflow
import pytest
from sklearn.metrics import roc_auc_score
import time

def test_challenger_beats_champion():
    # DEPLOYMENT GATE: challenger must not be significantly worse than champion.
    champion   = mlflow.sklearn.load_model("models:/fraud_detector/Production")
    challenger = mlflow.sklearn.load_model("models:/fraud_detector/Staging")

    X_test, y_test = load_held_out_test_set()  # always the same test set

    champion_auc   = roc_auc_score(y_test, champion.predict_proba(X_test)[:,1])
    challenger_auc = roc_auc_score(y_test, challenger.predict_proba(X_test)[:,1])

    print(f"Champion:   AUC={champion_auc:.4f}")
    print(f"Challenger: AUC={challenger_auc:.4f}")

    assert challenger_auc >= champion_auc - 0.005, (
        f"Challenger ({challenger_auc:.4f}) significantly worse than "
        f"champion ({champion_auc:.4f}). Blocking deployment."
    )

def test_challenger_latency_acceptable():
    # New model can't be 50% slower than champion.
    champion   = mlflow.sklearn.load_model("models:/fraud_detector/Production")
    challenger = mlflow.sklearn.load_model("models:/fraud_detector/Staging")

    X_sample = load_held_out_test_set()[0][:100]

    start = time.time(); champion.predict_proba(X_sample)
    champion_ms = (time.time() - start) * 1000

    start = time.time(); challenger.predict_proba(X_sample)
    challenger_ms = (time.time() - start) * 1000

    assert challenger_ms < champion_ms * 1.5, (
        f"Challenger {challenger_ms:.0f}ms vs champion {champion_ms:.0f}ms "
        f"({challenger_ms/champion_ms:.1f}× slower). Blocking deployment."
    )
```

---

**Next:** [04 -- Debugging ML →](04-debugging-ml.md)
""")

write("practical-skills/04-debugging-ml.md", """
# 04 -- Debugging ML Systems

> ML debugging is different from software debugging because failures are often silent and statistical. Use a systematic approach.

---

## The Outside-In Debugging Framework

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
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \\
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
""")

write("practical-skills/05-sql-for-mlops.md", """
# 05 -- SQL for MLOps Engineers

> SQL is used daily in MLOps -- for feature engineering, data quality checks, training data extraction, and production analysis.

---

## Feature Engineering Queries

```sql
-- User-level features for fraud detection model
-- This IS what your feature pipeline does
SELECT
    user_id,
    COUNT(*)                                             AS txn_count_30d,
    AVG(amount)                                          AS avg_amount_30d,
    MAX(amount)                                          AS max_amount_30d,
    STDDEV(amount)                                       AS std_amount_30d,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END)       AS fraud_count_30d,
    SUM(CASE WHEN is_foreign = 1 THEN 1 ELSE 0 END)     AS foreign_txn_count_30d,
    AVG(CASE WHEN is_foreign = 1 THEN 1.0 ELSE 0 END)   AS foreign_txn_rate_30d,
    MAX(transaction_time)                                AS last_transaction_time
FROM transactions
WHERE transaction_time >= NOW() - INTERVAL '30 days'
  AND user_id IS NOT NULL
  AND amount > 0
GROUP BY user_id;
```

---

## Window Functions -- Essential for ML

Window functions compute rolling statistics without collapsing rows.

```sql
SELECT
    user_id,
    transaction_time,
    amount,

    -- Rolling 7-transaction average for this user (time-ordered)
    AVG(amount) OVER (
        PARTITION BY user_id
        ORDER BY transaction_time
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS avg_last_7_txns,

    -- Time since previous transaction (in hours)
    EXTRACT(EPOCH FROM (
        transaction_time - LAG(transaction_time) OVER (
            PARTITION BY user_id ORDER BY transaction_time
        )
    )) / 3600 AS hours_since_last_txn,

    -- Running total for user this month
    SUM(amount) OVER (
        PARTITION BY user_id, DATE_TRUNC('month', transaction_time)
        ORDER BY transaction_time
    ) AS running_monthly_total,

    -- Rank by amount for this user (largest = rank 1)
    RANK() OVER (
        PARTITION BY user_id
        ORDER BY amount DESC
    ) AS amount_rank

FROM transactions
WHERE transaction_time >= '2024-01-01';
```

---

## Data Quality Queries (Run Before Every Training Job)

```sql
-- 1. Null rates per column
SELECT
    COUNT(*)                                                        AS total_rows,
    SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS user_id_null_pct,
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*)  AS amount_null_pct,
    SUM(CASE WHEN is_fraud IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS label_null_pct
FROM transactions
WHERE transaction_time >= NOW() - INTERVAL '7 days';

-- 2. Class balance
SELECT
    is_fraud,
    COUNT(*)                                              AS count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()             AS percentage
FROM transactions
GROUP BY is_fraud;

-- 3. Duplicate detection
SELECT transaction_id, COUNT(*) AS occurrences
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1
LIMIT 20;  -- any rows here = problem

-- 4. Distribution statistics for drift monitoring
SELECT
    PERCENTILE_CONT(0.01) WITHIN GROUP (ORDER BY amount) AS p01,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY amount) AS p50,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) AS p75,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY amount) AS p99,
    AVG(amount)                                            AS mean,
    STDDEV(amount)                                         AS std_dev
FROM transactions
WHERE transaction_time >= NOW() - INTERVAL '7 days';
```

---

## CTEs -- Readable Multi-Step Queries

```sql
-- Build training dataset step by step (readable, maintainable)
WITH
-- Step 1: Recent transactions
recent_transactions AS (
    SELECT *
    FROM transactions
    WHERE transaction_time BETWEEN '2024-01-01' AND '2024-06-30'
      AND amount > 0
),

-- Step 2: User-level features
user_features AS (
    SELECT
        user_id,
        COUNT(*)         AS txn_count,
        AVG(amount)      AS avg_amount,
        SUM(is_fraud)    AS fraud_count
    FROM recent_transactions
    GROUP BY user_id
),

-- Step 3: Join with user profile
enriched AS (
    SELECT
        uf.*,
        up.credit_score,
        up.account_age_days,
        up.country
    FROM user_features uf
    LEFT JOIN user_profiles up ON uf.user_id = up.user_id
)

-- Final: select features for training
SELECT * FROM enriched
WHERE txn_count >= 5    -- only users with enough history
  AND credit_score IS NOT NULL;
```

---

## JOINs for ML Data Preparation

```sql
-- LEFT JOIN: keep all transactions even if user profile missing
SELECT
    t.transaction_id,
    t.user_id,
    t.amount,
    t.is_fraud,                  -- ← label

    -- User profile features (NULL if profile missing → impute later)
    u.credit_score,
    u.account_age_days,
    u.country,

    -- Merchant features
    m.merchant_fraud_rate_90d,
    m.merchant_category

FROM transactions t
LEFT JOIN user_profiles u   ON t.user_id = u.user_id
LEFT JOIN merchant_stats m  ON t.merchant_id = m.merchant_id
WHERE t.transaction_time >= '2024-01-01'
  AND t.transaction_time <  '2024-07-01';
```

---

## Production Monitoring Queries

```sql
-- Model prediction distribution: is the model behaving normally?
SELECT
    DATE_TRUNC('hour', predicted_at)      AS hour,
    COUNT(*)                               AS total_predictions,
    AVG(fraud_probability)                 AS avg_fraud_prob,
    SUM(CASE WHEN fraud_probability > 0.5 THEN 1 ELSE 0 END) AS flagged_count,
    SUM(CASE WHEN fraud_probability > 0.5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS flag_rate
FROM model_predictions
WHERE predicted_at >= NOW() - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', predicted_at)
ORDER BY hour;
-- Alert if flag_rate changes significantly from historical average
```

---

**Next:** [06 -- Async Python →](06-async-python.md)
""")

write("practical-skills/06-async-python.md", """
# 06 -- Async Python, Pydantic & Error Handling

> FastAPI runs on async Python. Without understanding these patterns, you'll write serving code with hard-to-find performance bugs.

---

## Why Async Matters for ML Serving

```python
# SYNCHRONOUS: server blocks while waiting for Redis
def get_features(user_id):
    features = redis.get(user_id)     # blocks entire thread for 5ms
    return features                    # during this 5ms, NO other requests handled

# At 1000 req/s, this creates a massive backlog

# ASYNC: server handles other requests while waiting
async def get_features(user_id):
    features = await redis.get(user_id)  # yields control while waiting
    return features                       # other requests run during the wait
```

---

## Core Async Patterns

```python
import asyncio

# Run multiple I/O operations concurrently (not sequentially)
async def get_all_features(user_id: str, merchant_id: str):
    # Sequential: 5ms + 5ms = 10ms
    # user_features = await redis.hgetall(f"user:{user_id}")
    # merchant_features = await redis.hgetall(f"merchant:{merchant_id}")

    # Concurrent: max(5ms, 5ms) = 5ms (2× faster)
    user_features, merchant_features = await asyncio.gather(
        redis.hgetall(f"user:{user_id}"),
        redis.hgetall(f"merchant:{merchant_id}")
    )
    return user_features, merchant_features
```

---

## Pydantic -- Input Validation

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class PredictionRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0, lt=1_000_000,
                         description="Transaction amount in USD")
    merchant_category: str = Field(..., min_length=1)
    is_foreign: bool
    hour_of_day: int = Field(..., ge=0, le=23)
    credit_score: Optional[int] = Field(None, ge=300, le=850)

    @validator("merchant_category")
    def must_be_valid_category(cls, v):
        valid = {"retail", "restaurant", "travel", "online", "atm", "other"}
        if v.lower() not in valid:
            raise ValueError(f"Invalid category '{v}'. Must be one of {valid}")
        return v.lower()

    class Config:
        extra = "forbid"    # reject unknown fields (prevents injection)

# FastAPI uses Pydantic automatically
# Bad input → 422 Unprocessable Entity (never reaches your code)
# Good input → typed Python object (always correct types)
```

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
""")

# ─────────────────────────────────────────────────────────────────────────────
# CAREER
# ─────────────────────────────────────────────────────────────────────────────
write("career/01-interview-guide.md", """
# 01 -- MLOps Interview Guide

> MLOps interviews test whether you've actually built and operated these systems -- not just read about them. Specific examples beat vague knowledge every time.

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
""")

write("career/02-portfolio-strategy.md", """
# 02 -- Portfolio Strategy & Career Growth

> The engineers who reach top 0.1% build in public, contribute to open source, and let their work speak for them.

---

## The GitHub Portfolio Structure

Every project should follow this structure:

```
fraud-detection-mlops/
├── README.md               ← CRITICAL: first thing everyone reads
│   ├── What problem this solves (1 sentence)
│   ├── Architecture diagram (draw.io or mermaid)
│   ├── Tech stack with versions
│   ├── Measured results (latency, throughput, cost)
│   └── How to run it
├── src/
│   ├── features/           ← feature engineering code
│   ├── training/           ← training pipeline
│   └── serving/            ← serving code + Dockerfile
├── infrastructure/
│   ├── k8s/                ← Kubernetes manifests
│   └── terraform/          ← infrastructure as code
├── tests/                  ← all test levels (data, model, pipeline, gate)
└── docs/
    └── architecture.md     ← Architecture Decision Records
```

---

## Technical Blog Strategy

One blog post per completed project. Target: 1 post/month.

**What makes a blog post get read and shared:**

```
NOT: "Here's how MLflow works" (already covered everywhere)

YES: "Why our MLflow tracking server was losing runs under high load --
      and how we fixed it with connection pooling"

YES: "The subtle feature store bug that caused training-serving skew
      for 3 months before we caught it"

YES: "How I built a production MLOps stack for under $50/month on a VPS"
      (your unique Nepal/VPS angle -- nobody else has this story)
```

**Blog post structure that works:**

```
Title: Specific problem + what you did about it
       "How I reduced model serving costs 80% with ONNX quantization"

Hook (100 words): The problem and why it matters

The Story (300 words):
  - What you tried first and why it didn't work
  - The insight that unlocked the solution

The Solution (400 words):
  - Architecture or approach
  - Key code snippet (production quality)

The Results (100 words):
  - Before/after numbers (latency, cost, throughput)
  - What you'd do differently

Conclusion (50 words): Next steps, what you learned
```

---

## LinkedIn Post Template for Projects

```
Just shipped: [Project Name] 🚀

Problem I solved:
[One sentence describing the business/engineering problem]

What I built:
• [Technical component 1]
• [Technical component 2]
• [Technical component 3]

Stack: [Tool 1] + [Tool 2] + [Tool 3] + [Tool 4]

Results:
• [Metric 1]: before → after (X% improvement)
• [Metric 2]: before → after

Full writeup: [blog link]
Code: [github link]

#MLOps #MachineLearning #DevOps #Python
```

---

## Open Source Contribution Path

Start small. Don't start with features.

```
Month 1: Documentation fixes
  → Use the tool seriously
  → When something confuses you, the docs are wrong/missing
  → Fix them. PR merged in < 48h usually.

Month 2: Bug reproductions
  → Find an open issue with vague reproduction steps
  → Reproduce it, add minimal reproduction script
  → Comment in the issue: "I reproduced this with: ..."
  → Maintainers love this -- no code change needed

Month 3: Fix a "good first issue"
  → Every serious OSS project labels these
  → Small, scoped, maintainer willing to guide you

Month 4+: Small bug fixes, then features
  → Comment BEFORE implementing: "I'd like to fix this by X approach"
  → Get maintainer buy-in before writing code

Target projects for MLOps: Feast, Evidently AI, Prefect, MLflow, ZenML
```

---

## The Outreach Message That Gets Responses

```
Subject: ML Platform Engineer -- [something specific about them]

Hi [Name],

I noticed [company] is [specific thing you observed -- recent job post,
blog post, open source project they use] related to ML infrastructure.

I'm an MLOps/ML Platform engineer specializing in Kubernetes-native ML
systems -- specifically the gap between "model works in notebook" and
"model is reliable in production."

What I've shipped recently:
• Feature store (Feast + Redis) serving sub-20ms predictions [GitHub]
• Automated CT pipeline with drift-based triggers, reducing manual
  retraining from weekly manual effort to fully automated [Blog post]
• Shadow → canary deployment framework that cut production incidents 60% [GitHub]

I'm based in Nepal, available for remote work, timezone UTC+5:45
(good overlap with EU and partial overlap with US East).

Would a 20-minute call make sense?

Suchan
suchanmadhikarmi.com.np | github.com/SuchanMadhikarmi
```

---

## The 24-Month Blueprint

**Months 1-6:** Build Projects P-01 to P-06 publicly on GitHub
  → 6 public repos with clean READMEs
  → 6 blog posts (one per project)
  → Start appearing in MLOps Slack communities

**Months 7-12:** Advanced projects + first open source contribution
  → Projects P-07, P-08
  → Merged PR in Feast or Evidently
  → Write your defining post: "How I built production MLOps for $50/month"

**Months 13-18:** Projects P-09, P-10 + niche authority
  → Kubernetes-native MLOps is your specialty
  → Active in community (answering questions, GitHub issues)
  → Recruiters start appearing in your LinkedIn

**Months 19-24:** First USD remote opportunity
  → 9 public projects + 15+ blog posts + 2-3 OSS contributions
  → Direct outreach to 20 ML-heavy Series B/C startups
  → First contract or role landed → the flywheel starts

---
""")

# ─────────────────────────────────────────────────────────────────────────────
# PROJECTS
# ─────────────────────────────────────────────────────────────────────────────
write("projects/10-portfolio-projects.md", """
# 10 Portfolio Projects -- Complete Specifications

Build these in order. Each project teaches the concepts from the previous one in a new context.

---

## P-01 -- Full MLflow Pipeline on Docker

**Level:** 🟢 Foundation | **Impact:** 4/10 | **Time:** 1-2 weeks

**What you build:** A production-grade MLflow setup with proper backend and artifact storage.

**Architecture:**
```
MLflow Tracking Server → PostgreSQL (metadata)
                       → MinIO/S3 (model artifacts)
Training Script → MLflow (auto-logs all runs)
MLflow UI → Query and compare experiments
```

**Requirements:**
- MLflow server with PostgreSQL backend (not SQLite -- that's not production)
- MinIO as artifact store (S3-compatible, self-hosted)
- Docker Compose bringing all services up together
- Training script that auto-logs: git hash, data hash, all hyperparameters, metrics, model
- Model registered to MLflow Model Registry with staging/production stages

**Evaluation criteria:**
- `docker compose up` starts everything with no errors
- Training script creates a traceable run
- Model is loadable via `mlflow.sklearn.load_model("models:/model-name/Production")`
- Can reproduce any historical run from the logged metadata

**Stack:** MLflow 2.x · PostgreSQL 14 · MinIO · Docker Compose · scikit-learn or XGBoost

---

## P-02 -- Versioned Data Pipeline with DVC

**Level:** 🟢 Foundation | **Impact:** 5/10 | **Time:** 1-2 weeks

**What you build:** A reproducible ML pipeline where data and models are versioned.

**Requirements:**
- DVC initialized with S3/MinIO remote storage
- At least 2 data versions tracked (simulate a data update)
- DVC pipeline (`dvc.yaml`) with stages: prepare → train → evaluate
- Great Expectations suite with at minimum 5 expectations
- Demonstrate: `git checkout old-commit && dvc checkout` reproduces old state exactly
- DVC metrics comparison: `dvc metrics diff HEAD~1`

**Key to get right:** The `.dvc` pointer files are in Git. Actual data is in MinIO. Switching git commits switches data versions.

**Stack:** DVC · Great Expectations · MinIO · Git

---

## P-03 -- Production Model Serving API

**Level:** 🟢 Foundation | **Impact:** 6/10 | **Time:** 1-2 weeks

**What you build:** A production-quality serving API with all the pieces a real deployment needs.

**Requirements:**
- FastAPI with Pydantic input validation (reject bad inputs with 422, not 500)
- Model loaded from MLflow Registry at startup (not baked into image)
- `/health`, `/ready`, `/predict`, `/metrics` endpoints
- Prometheus metrics: prediction count, latency histogram, error rate, fallback rate
- Structured JSON logging for every prediction (prediction_id, user_id, model_version, latency_ms)
- Graceful fallback: if model fails, return default prediction (not 500 error)
- Kubernetes Deployment with readiness and liveness probes
- Load test: demonstrate 100+ req/s with P99 < 100ms

**Stack:** FastAPI · Pydantic · MLflow · Prometheus · Kubernetes · Docker

---

## P-04 -- Automated ML CI/CD Pipeline

**Level:** 🔵 Core | **Impact:** 7/10 | **Time:** 2 weeks

**What you build:** A GitHub Actions pipeline that trains, evaluates, and deploys models automatically.

**Pipeline stages:**
```
Push to main
  → data-validation job (Great Expectations)
  → train job (pulls data via DVC, logs to MLflow)
  → evaluate job (challenger vs champion gate -- blocks if challenger loses)
  → build job (Docker image with SHA tag, push to registry)
  → deploy-staging job (automatic)
  → deploy-production job (requires manual approval in GitHub)
```

**Requirements:**
- All stages fail fast and clearly (not silently)
- Challenger vs champion comparison is the deployment gate
- Secrets managed via GitHub Secrets (never hardcoded)
- Slack notification on success/failure
- Manual approval gate before production deployment

**Stack:** GitHub Actions · MLflow · Docker · Kubernetes · DVC

---

## P-05 -- ML Observability Dashboard

**Level:** 🔵 Core | **Impact:** 7.5/10 | **Time:** 2 weeks

**What you build:** A Grafana dashboard that shows everything happening with your ML system.

**Dashboard panels:**
```
Row 1: Traffic
  - Predictions/second (rate)
  - Error rate % (with alert threshold)
  - P50/P95/P99 latency

Row 2: Model Health
  - Fraud prediction rate over time (should be stable)
  - Confidence distribution histogram
  - Fallback rate

Row 3: Feature Monitoring
  - Mean of top-5 features over time
  - Null rate per feature (alert if > 5%)

Row 4: Drift
  - PSI per feature (alert if > 0.2)
  - Prediction distribution shift metric
```

**Requirements:**
- Prometheus scraping serving API metrics
- Loki collecting structured prediction logs
- Evidently generating daily drift reports
- AlertManager sending Slack alerts when thresholds breached
- All dashboards as code (JSON files in repo)

**Stack:** Prometheus · Grafana · Loki · Evidently AI · AlertManager

---

## P-06 -- Automated Continuous Training Pipeline

**Level:** 🔵 Core | **Impact:** 8/10 | **Time:** 2-3 weeks

**What you build:** A fully automated system that detects drift, retrains, evaluates, and deploys -- without human intervention.

**Requirements:**
- Daily Prefect/Airflow job that checks drift (PSI on key features)
- If drift detected → triggers full CT pipeline (validate → train → evaluate gate → promote)
- Champion vs challenger evaluation with automatic blocking
- Post-deployment monitoring: watches for 48h, rolls back if metrics degrade
- Slack notifications at each major stage
- Full audit trail in MLflow

**The key thing that makes this advanced:** The system retrains AND validates AND deploys AND watches AND rolls back -- all automatically, end to end.

**Stack:** Prefect or Airflow · MLflow · Evidently · Kubernetes CronJob

---

## P-07 -- Shadow + Canary Deployment Framework

**Level:** 🟡 Advanced | **Impact:** 8.5/10 | **Time:** 2-3 weeks

**What you build:** A model routing layer that supports shadow testing and gradual canary rollouts.

**Requirements:**
- Shadow mode: both models run on every request, challenger prediction only logged
- Canary mode: configurable traffic split via hot-reloadable YAML config
- Consistent user assignment (same user always goes to same model in A/B test)
- Automatic rollback: if challenger error rate > 2% → rollback to champion automatically
- Side-by-side prediction comparison logged to structured store
- Grafana panel showing champion vs challenger metrics side by side

**The routing config is hot-reloadable: changing the YAML file shifts traffic within 30 seconds, no redeployment.**

**Stack:** FastAPI · Traefik or nginx · Redis · Prometheus · Grafana

---

## P-08 -- Feature Store (Online + Offline)

**Level:** 🟡 Advanced | **Impact:** 9/10 | **Time:** 3-4 weeks

**What you build:** A production-grade feature store that serves both training and real-time serving with identical feature definitions.

**Requirements:**
- Feast with PostgreSQL offline store and Redis online store
- At least 10 features defined across 2 entity types (user + merchant)
- Point-in-time correct feature retrieval for training (prevents feature leakage)
- Materialization job that syncs offline → online every hour (Kubernetes CronJob)
- Training script uses `get_historical_features()` (offline store)
- Serving API uses `get_online_features()` (Redis, < 5ms)
- Architecture Decision Record documenting design choices

**This project alone will differentiate you from 95% of MLOps candidates.**

**Stack:** Feast · Redis · PostgreSQL · Apache Parquet · Kubernetes

---

## P-09 -- Kubernetes-Native ML Pipeline (KFP + Argo)

**Level:** 🔴 Elite | **Impact:** 9.5/10 | **Time:** 4-6 weeks

**What you build:** A complete training pipeline where every step runs in its own Kubernetes pod with isolated resources.

**Pipeline steps:**
```
[Pod 1] Data Validation          2 CPU, 4GB RAM
[Pod 2] Feature Engineering      8 CPU, 32GB RAM
[Pod 3] Distributed Training     4× GPU, 256GB RAM, 32 CPU
[Pod 4] Model Evaluation         2 CPU, 8GB RAM
[Pod 5] Model Registration       1 CPU, 2GB RAM
[Pod 6] Canary Deployment Trigger 1 CPU, 1GB RAM
```

**Requirements:**
- KubeFlow Pipelines or Argo Workflows defining the DAG
- Each step in its own container with specific resource requests
- GPU scheduling for training step
- Inter-step artifact passing through MinIO
- Pipeline caching (unchanged steps skip re-execution)
- Integration with MLflow for experiment tracking

**Stack:** KubeFlow Pipelines or Argo Workflows · Kubernetes · GPU nodes · MLflow · MinIO

---

## P-10 -- Mini ML Platform (End-to-End)

**Level:** 🔴 Elite | **Impact:** 10/10 | **Time:** 8-12 weeks

**What you build:** Your magnum opus. A complete self-hosted ML platform combining everything from P-01 to P-09.

**The platform must provide:**
```
Input:  "I have a Python training script and a dataset"
Output: "Model is in production, monitored, and auto-retraining"
       (with one command or one UI click)
```

**Components:**
- Feature Store (Feast + Redis) ← from P-08
- Experiment Tracking (MLflow) ← from P-01
- Data Versioning (DVC) ← from P-02
- CI/CD Pipeline (GitHub Actions) ← from P-04
- K8s-Native Training (KFP/Argo) ← from P-09
- Model Serving Layer (FastAPI + ONNX) ← from P-03
- Shadow/Canary Deployment ← from P-07
- Observability Dashboard ← from P-05
- Continuous Training ← from P-06
- Infrastructure as Code (Terraform + Helm)

**Deliverables:**
1. Working platform deployed on your VPS or k3s cluster
2. Helm charts for all components
3. Terraform for infrastructure
4. 3,000-word technical blog post explaining the architecture
5. 5-minute video demo

**This is your portfolio centerpiece. It's what you show in interviews instead of answering questions.**
""")

# ─────────────────────────────────────────────────────────────────────────────
# QUICK REFERENCE
# ─────────────────────────────────────────────────────────────────────────────
write("QUICK-REFERENCE.md", """
# Quick Reference -- Checklists, Commands & Tables

---

## Pre-Deployment Checklist

```
□ Evaluated on held-out test set (not validation set)
□ Compared against production champion -- challenger wins or ties
□ Latency benchmarked -- meets SLA (P99 < 100ms?)
□ Memory profiled -- fits in production pod resources
□ model.eval() confirmed in serving code
□ Input validation (Pydantic) covers all edge cases
□ Graceful fallback defined for model errors
□ Prometheus metrics configured
□ Rollback procedure documented and tested
□ Alerts configured -- who gets paged at what threshold?
□ Model card written
□ Deployment contract signed with model owner
```

---

## PSI Thresholds

| PSI | Drift Level | Action |
|---|---|---|
| < 0.10 | None | Monitor normally |
| 0.10-0.20 | Moderate | Investigate, watch closely |
| ≥ 0.20 | Significant | Trigger retraining |

---

## Key Kubernetes Commands

```bash
# Pod debugging
kubectl logs <pod> --tail=100
kubectl logs <pod> --previous              # crashed container
kubectl exec -it <pod> -- /bin/bash        # shell inside container
kubectl describe pod <pod>                 # why is it pending/failing?

# Resource monitoring
kubectl top pods --sort-by=memory
kubectl top nodes

# Deployments
kubectl rollout status deployment/<name>   # watch rollout
kubectl rollout undo deployment/<name>     # instant rollback
kubectl scale deployment <name> --replicas=5

# Port forwarding
kubectl port-forward svc/mlflow-service 5000:5000
kubectl port-forward svc/fraud-serving 8000:8000

# GPU inside pod
kubectl exec <pod> -- nvidia-smi
kubectl exec <pod> -- python -c "import torch; print(torch.cuda.memory_allocated()/1e9, 'GB')"
```

---

## Log Levels -- Use Correctly

| Level | When | Always On? |
|---|---|---|
| DEBUG | Detailed debugging (feature values, intermediate steps) | No -- off in production |
| INFO | Normal operation (prediction made, model loaded) | Yes |
| WARNING | Something unusual (high null rate, using fallback) | Yes |
| ERROR | Something broke (inference failed, DB timeout) | Yes |
| CRITICAL | System cannot operate (model registry down) | Yes |

---

## Tool Comparison Tables

### Experiment Tracking

| Tool | Self-hosted | Cost | Best For |
|---|---|---|---|
| MLflow | ✅ Easy | Free | Production, enterprise |
| W&B | ✅ Complex | Free tier → paid | Research, visualization |
| Neptune | ✅ | Free tier → paid | Collaboration |
| ClearML | ✅ | Free | Full MLOps platform |

### Pipeline Orchestration

| Tool | Type | Best For |
|---|---|---|
| Airflow | Traditional DAG | Batch pipelines, mature ecosystem |
| Prefect | Modern Python | Easier development, good UI |
| KFP | K8s-native | Enterprise ML, GPU scheduling |
| Argo Workflows | K8s-native | Container-first, general purpose |
| ZenML | ML-focused | Simple MLOps, quick setup |

### Model Serving

| Tool | Type | Best For |
|---|---|---|
| FastAPI | Framework | Custom serving logic, simplicity |
| BentoML | ML-focused | Quick deployment, batching |
| Triton | High-performance | Multi-model, GPU, enterprise |
| TorchServe | PyTorch-native | Pure PyTorch models |
| vLLM | LLM-specialized | High-throughput LLM serving |

### Drift Monitoring

| Tool | Type | Best For |
|---|---|---|
| Evidently AI | Open source | Full drift + quality reports |
| WhyLogs | Open source | Lightweight, logging-based |
| Arize | Managed | Enterprise observability |
| Fiddler | Managed | Explainability + monitoring |

---

## The Vocabulary Bridge

| Data Scientist Says | MLOps Engineer Understands |
|---|---|
| "Model isn't converging" | Training loss not decreasing -- check LR, data quality |
| "We're overfitting" | Val loss >> train loss → need regularization or more data |
| "Features are leaking" | Training-serving skew or target leakage → audit feature pipeline |
| "I need to run a sweep" | Distributed parallel jobs with Ray Tune or Optuna |
| "I need more GPU memory" | Higher VRAM instance or model parallelism |
| "Predictions are biased" | Fairness metrics across groups -- run Fairlearn analysis |
| "We need to retrain more" | Shorter CT interval + shorter label feedback loop |
| "Model is poorly calibrated" | Reliability diagram miscalibration → Platt scaling |

---

## Serialization Format Guide

| Model | Training | Production Serving | Never Use |
|---|---|---|---|
| sklearn | joblib | ONNX Runtime | pickle (security) |
| XGBoost | .ubj native | ONNX Runtime | pickle |
| PyTorch | SafeTensors | ONNX → TensorRT | torch.save with pickle |
| HuggingFace | SafeTensors | vLLM / TGI | pickle |

---

## Memory Cheat Sheet

```
7B model memory requirements:
  FP32:  28 GB  (doesn't fit in single 24GB GPU)
  FP16:  14 GB  (fits in A100 40GB)
  INT8:   7 GB  (fits comfortably)
  INT4:   3.5 GB (runs on consumer GPU)

Training memory ≈ inference memory × 3-4
(model + gradients + optimizer states)

GPU VRAM OOM fix:    reduce batch size first
Container OOM fix:   increase memory limits in K8s spec
```
""")

# ─────────────────────────────────────────────────────────────────────────────
# CONTRIBUTING
# ─────────────────────────────────────────────────────────────────────────────
write("CONTRIBUTING.md", """
# Contributing to MLOps Complete Guide

Thank you for your interest in contributing! This guide is meant to be the most practical, production-focused MLOps resource available. Your contributions help engineers worldwide.

---

## Ways to Contribute

### 🐛 Fix Errors
Found incorrect information, outdated code, or a typo? Open an issue or submit a PR directly. Small fixes are always welcome.

### 📖 Improve Explanations
Found something confusing? Rewrite it more clearly. The goal is that any DevOps engineer can understand every concept without prior ML knowledge.

### 💻 Add Code Examples
Add production-quality code examples to existing guides. Requirements:
- Must be production-grade (proper error handling, logging, types)
- Must include comments explaining WHY, not just what
- Must work with the library versions specified in the guide

### 🆕 Add New Sections
Topics not yet covered:
- Feature engineering for specific domains (NLP, time-series, tabular)
- Specific cloud provider deep-dives
- ML cost optimization case studies
- Real production incident post-mortems

### 🌍 Translations
Translating sections to other languages (especially Hindi, Nepali) would make this accessible to more engineers.

---

## Contribution Guidelines

### Code Standards
- Python 3.10+
- Type hints on all function signatures
- Docstrings on all public functions
- Production-grade error handling (no bare `except:`)
- Tested locally before submitting

### Markdown Standards
- Keep sections scannable (tables, code blocks, headers)
- Code blocks should specify the language for syntax highlighting
- Include the "Why this matters for MLOps" context -- not just the what

### What We Don't Accept
- Purely theoretical content without practical application
- Code that isn't tested and working
- Promotional content for specific vendors
- Beginner Python tutorials (assume Python competence)

---

## How to Submit

1. Fork the repository
2. Create a branch: `git checkout -b improve/section-name`
3. Make your changes
4. Test any code examples locally
5. Submit a PR with a clear description of what you changed and why

---

## Code of Conduct

- Be respectful and constructive in all communications
- Focus on the technical content, not the person
- Beginner questions are welcome -- we were all there once

---

**Questions?** Open a GitHub Issue or reach out on LinkedIn.
""")

# ─────────────────────────────────────────────────────────────────────────────
# LICENSE
# ─────────────────────────────────────────────────────────────────────────────
write("LICENSE", """
MIT License

Copyright (c) 2024 Suchan Madhikarmi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

# ─────────────────────────────────────────────────────────────────────────────
# .gitignore
# ─────────────────────────────────────────────────────────────────────────────
write(".gitignore", """
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.venv/
venv/
env/
*.egg-info/
dist/
build/

# Data (track with DVC)
*.csv
*.parquet
*.feather
*.h5
*.hdf5
data/raw/
data/processed/

# Models (track with DVC or MLflow)
*.pkl
*.joblib
*.onnx
*.pt
*.pth
*.safetensors
*.bin
models/

# MLflow
mlruns/
mlartifacts/

# DVC
.dvc/cache/
.dvc/tmp/

# Secrets -- NEVER commit these
.env
.env.*
*.key
*.pem
secrets.yaml
secrets.json
*_credentials.json
*_credentials.yaml

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Terraform
*.tfstate
*.tfstate.backup
.terraform/

# Docker
.docker/
""")

print("\n" + "="*60)
print("✅  Repository created successfully!")
print("="*60)

import os
total_files = sum(len(files) for _, _, files in os.walk("."))
total_dirs = sum(len(dirs) for _, dirs, _ in os.walk("."))
print(f"\n📁  Directories: {total_dirs}")
print(f"📄  Files:       {total_files}")

print("""
Next steps:
  1. cd into this folder
  2. git init
  3. git add .
  4. git commit -m "Initial commit: MLOps Complete Guide"
  5. Create repo on GitHub: github.com/new
  6. git remote add origin https://github.com/SuchanMadhikarmi/mlops-complete-guide.git
  7. git branch -M main
  8. git push -u origin main
  9. Add repo description and topics on GitHub
 10. Share on LinkedIn!

GitHub repo topics to add:
  mlops, machine-learning, devops, kubernetes, mlflow,
  feast, python, production-ml, deep-learning, llmops
""")
