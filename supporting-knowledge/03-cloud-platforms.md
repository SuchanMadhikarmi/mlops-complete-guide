# 03 — Cloud ML Platforms

## Prerequisites

**AWS/GCP/Azure knowledge:** Familiar with at least one cloud platform (AWS recommended). Have created S3 buckets, understand IAM basics.

**MLOps context:** Know the difference between "managed services" (no infrastructure to manage) and "self-hosted" (you run everything).

**Required understanding:** When to buy managed vs build custom. Core concepts are the same across all platforms.

> You don't need to master all three. You need to know what each offers, the shared concepts, and when to use managed vs self-hosted.

## The Build vs Buy Decision

| Factor | Self-Hosted (K8s + OSS) | Managed (SageMaker/Vertex) |
|---|---|---|
| Cost at scale | Lower (no markup) | Higher (significant markup) |
| Operational burden | High (you manage everything) | Low (cloud manages infra) |
| Flexibility | Complete | Limited to platform features |
| Vendor lock-in | None | High |
| Setup time | Weeks | Hours |
| Team needed | Platform engineers | Small team |
| Data residency | Full control | Depends on region/config |

**Rule of thumb:**
- < 10 ML engineers, moving fast → use managed (SageMaker/Vertex)
- 10+ engineers, need control, data is sensitive → build on Kubernetes
- Most companies → hybrid (managed for commodity, custom for differentiating)

---

## AWS SageMaker

### Core Components

| Component | What It Does | OSS Equivalent |
|---|---|---|
| Studio | Web IDE for ML | JupyterHub |
| Training Jobs | Run training on managed compute | K8s Jobs |
| Experiments | Track runs, metrics, artifacts | MLflow |
| Feature Store | Online + offline feature store | Feast + Redis |
| Model Registry | Version and approve models | MLflow Registry |
| Endpoints | Deploy models as REST APIs | FastAPI + K8s |
| Batch Transform | Batch inference on S3 data | K8s Jobs |
| Pipelines | Build ML pipelines as code | KubeFlow Pipelines |
| Model Monitor | Monitor for data drift | Evidently AI |

### Key SageMaker Patterns

```python
import sagemaker
from sagemaker.sklearn import SKLearn
from sagemaker.model_monitor import DataCaptureConfig

session = sagemaker.Session()
role = "arn:aws:iam::123456789:role/SageMakerRole"

# Training job
estimator = SKLearn(
    entry_point="train.py",
    role=role,
    instance_type="ml.m5.xlarge",
    framework_version="1.2-1",
    hyperparameters={"n-estimators": 300, "max-depth": 6}
)

estimator.fit({"train": "s3://bucket/train/", "test": "s3://bucket/test/"})

# Deploy with data capture (for monitoring)
data_capture_config = DataCaptureConfig(
    enable_capture=True,
    sampling_percentage=100,
    destination_s3_uri="s3://bucket/capture/"
)

predictor = estimator.deploy(
    initial_instance_count=2,
    instance_type="ml.m5.large",
    data_capture_config=data_capture_config
)
```

---

## Google Cloud Vertex AI

### Core Components

| Component | What It Does |
|---|---|
| Workbench | Managed Jupyter notebooks |
| Custom Training | Submit training to managed compute |
| Experiments | Experiment tracking |
| Feature Store | Managed feature store (BigQuery backend) |
| Model Registry | Model versioning |
| Endpoints | Deploy for online prediction |
| Batch Prediction | Large-scale offline inference |
| Pipelines | KubeFlow Pipelines managed |
| Model Monitoring | Drift detection |

### Vertex AI Advantage

BigQuery → Vertex AI Feature Store integration is best-in-class. If your data is in BigQuery, Vertex AI is the natural choice.

```python
from google.cloud import aiplatform

aiplatform.init(project="my-project", location="us-central1")

# Submit training job
job = aiplatform.CustomTrainingJob(
    display_name="fraud-detector-training",
    script_path="train.py",
    container_uri="us-docker.pkg.dev/vertex-ai/training/sklearn-cpu.1-0:latest",
    requirements=["xgboost", "mlflow"],
    model_serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest"
)

model = job.run(
    dataset=dataset,
    machine_type="n1-standard-4",
    replica_count=1,
)

# Deploy endpoint
endpoint = model.deploy(
    deployed_model_display_name="fraud-detector-v24",
    machine_type="n1-standard-2",
    min_replica_count=1,
    max_replica_count=5,
    traffic_split={"0": 100}
)
```

---

## Azure Machine Learning

### Core Components

Same capabilities as SageMaker and Vertex AI. Strongest advantages:

1. **Enterprise integration** — Azure AD, DevOps, Teams
2. **Responsible AI Dashboard** — Best fairness/explainability UI
3. **Hybrid deployment** — Seamless on-prem + cloud

```python
from azure.ai.ml import MLClient, command
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="...",
    resource_group_name="rg-mlops",
    workspace_name="ws-fraud-detection"
)

# Submit training job
job = command(
    code="./src",
    command="python train.py --data ${{inputs.training_data}}",
    inputs={"training_data": Input(type="uri_folder", path="azureml://...")},
    environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest",
    compute="cpu-cluster",
    display_name="fraud-detector-training"
)

returned_job = ml_client.jobs.create_or_update(job)
```

---

## The Shared Concepts Across All Three

Once you understand one, the others are just different APIs for the same concepts:

```
Concept              AWS SageMaker          GCP Vertex AI          Azure ML
──────────────────────────────────────────────────────────────────────────────
Notebooks            Studio                 Workbench              Studio
Training             Training Jobs          Custom Training        Compute Clusters
Experiment tracking  Experiments            Experiments            Experiments
Feature store        Feature Store          Feature Store          Feature Store
Model registry       Model Registry         Model Registry         Model Registry
Online serving       Endpoints              Endpoints              Online Endpoints
Batch serving        Batch Transform        Batch Prediction       Batch Endpoints
Pipeline             Pipelines              Vertex Pipelines       ML Pipelines
Monitoring           Model Monitor          Model Monitoring       Monitoring
```

---

**Next:** [04 — ML Security →](04-ml-security.md)
