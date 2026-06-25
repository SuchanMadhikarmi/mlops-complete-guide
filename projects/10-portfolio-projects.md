# 10 Portfolio Projects -- Complete Specifications

## Prerequisites

**What you need before starting:** Have completed the ML fundamentals section. Have trained and deployed at least 1 model end-to-end. Can write Python, understand basic SQL, familiar with Git.

**Why projects matter:** Recruiters don't believe job descriptions. They believe working code. These 10 projects prove you can build production ML systems.

**The progression:** P-01 to P-05 are foundation skills. P-06 to P-08 are advanced. P-09 to P-10 are elite tier. Do them in order.

> Build these in order. Each project teaches the concepts from the previous one in a new context.

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

**Why this matters:** Real companies don't use SQLite for MLflow. This teaches you production infrastructure.

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

**Why this matters:** Data versioning is how you achieve reproducibility at scale.

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

**Why this matters:** Real serving isn't just loading a model. It's observability, error handling, and graceful degradation.

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

**Why this matters:** Automation is how you move fast safely. This is the difference between 1 deployment/quarter and 10 deployments/week.

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

**Why this matters:** You can't manage what you don't measure. This teaches observability culture.

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

**Why this matters:** This is where companies move from "deploy once a quarter" to "model updates happen continuously." Game changer for model performance.

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

**Why this matters:** This is how Netflix, Airbnb, and Uber deploy models safely. You learn the same patterns they use.

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

**Why this matters:** Feature stores are the bridge between data and models. Getting this right is what separates junior and senior MLOps engineers.

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

**Why this matters:** This is enterprise-grade ML infrastructure. Companies that do this well scale from 1 model to 100 models easily.

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

**Why this matters:** This is your portfolio centerpiece. It's what you show in interviews instead of answering questions. One look at this codebase tells experienced engineers: "This person knows their stuff."

---
