# 05 -- ML Platform Design Patterns

## Prerequisites

**Core MLOps knowledge:** Understand experiment tracking (MLflow), model serving, continuous training concepts. Have built at least 3 complete ML systems end-to-end.

**DevOps/SRE perspective:** Familiar with microservices architecture, observability, deployment strategies, infrastructure-as-code concepts.

**Required tools:** Kubernetes · Terraform or CloudFormation · Your choice of MLflow, DVC, or equivalent

> An ML platform is the infrastructure, tooling, and workflows that let data scientists develop, train, deploy, and monitor models -- without managing infrastructure themselves.

## Why This Matters (The SRE Translation)

Building an ML platform is like building an internal platform for your engineering team:

- Without it: Data scientists manage their own infrastructure, dependencies, deployments. Chaos. Inconsistent practices. High maintenance burden on engineers.
- With it: Data scientists run `platform.train()` and `platform.deploy()`, infrastructure is abstracted. Consistent practices. Scalable.

Companies that master this (Netflix, Uber, Airbnb, Square) gain massive competitive advantage.

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

**Operational benefit:** If your database goes down, training jobs keep running. If storage fails, compute spins back up when fixed. Failure is isolated.

### 2. Everything as Code

```yaml
# ALL configuration in Git -- never in a UI only
training_config.yaml      → training parameters
serving_config.yaml        → deployment config
monitoring_thresholds.yaml → alert thresholds
feature_definitions.py     → Feast feature definitions
pipeline_definition.py     → KFP pipeline
```

**DevOps benefit:** Git history is your audit trail. "Who changed the alert threshold and when?" Answer: check Git. Compare platform configs across environments: trivial with code.

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

**Impact:** New data scientist learns platform in 1 day, not 1 month. Trains first model in 1 week, not 1 month.

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
- **Compliance:** GDPR, EU AI Act require explainability. Full lineage enables this.
- **Debugging:** "Why did behavior change after last week's deployment?" Trace back through lineage.
- **Reproducibility:** "Reproduce the model from 6 months ago" -- all metadata is available.

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
