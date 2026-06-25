# 02 -- Kubernetes-Native ML (KFP + Argo)

## Prerequisites

**From DevOps/Kubernetes perspective:** Familiar with Kubernetes concepts (Pods, deployments, resource requests/limits). If not, read [practical-skills/02-kubernetes-for-ml.md](../../practical-skills/02-kubernetes-for-ml.md) first.

**From ML perspective:** Know what MLflow pipelines are and why continuous training is needed. Have deployed at least one model.

**Required tools:** kubectl · Kubernetes cluster (1.20+) · Docker · Helm

> In Kubernetes-native ML, every pipeline step runs in its own isolated container with its own resource allocation. This is enterprise-grade ML infrastructure.

## Why This Matters (The DevOps Translation)

Think of Kubernetes-native ML like how you manage microservices:

- Each microservice gets its own pod, CPU/memory allocation, and can fail independently
- Kubernetes native ML applies the same logic to training pipeline steps
- A data validation step doesn't need 8 GPUs, so it requests only 2 CPUs
- A training step requests exactly 4 GPUs, and Kubernetes schedules it on a node that has them
- One step crashing doesn't affect other steps (isolation)

This is why enterprise ML teams use it: **separation of concerns + resource efficiency + fault isolation**.

---

## Why Not Just Use Airflow for ML?

| Airflow | Kubernetes-Native (KFP/Argo) |
|---|---|
| All tasks share same Python environment | Every step in its own container |
| All tasks share same compute resources | Each step gets exactly the resources it needs |
| Training step can't request 8 GPUs easily | Training step requests `nvidia.com/gpu: 8` |
| One failure can affect other running tasks | Complete isolation -- failures don't spread |
| Limited caching | Built-in step caching (skip unchanged steps) |

**Production consequence:** With Airflow, a data validation script with a memory leak could gradually consume all cluster memory, affecting other tasks. With Kubernetes-native, each task is containerized -- the leak affects only that pod.

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

### Code Walkthrough: Why Each Line Matters

```python
@component(
    base_image="nvcr.io/nvidia/pytorch:23.10-py3",  # NVIDIA's official PyTorch image
    packages_to_install=["mlflow", "scikit-learn"]   # Installed at container build time
)
def train_model(...):
    # Each time this component runs:
    # 1. A new pod is created from the base image
    # 2. packages_to_install are pip installed
    # 3. The function code runs
    # 4. Pod is destroyed
    # This isolation means: one job can't affect another's dependencies
```

**Production consequence:** If you update scikit-learn version, old training runs still use the old version. New runs use the new version. Perfect reproducibility.

```python
train_task.set_accelerator_type("NVIDIA_TESLA_A100").set_accelerator_limit(4)
# Kubernetes schedules this pod only on nodes with 4 available A100 GPUs
# If no node has 4 A100s, the pod waits (queues) until one becomes available
# Without this: training would run on CPU, 100x slower, wasting money
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

### Why Argo Over KFP?

- **Argo:** More Kubernetes-native, uses standard K8s YAML, simpler learning curve
- **KFP:** Pythonic, better for data scientists, integrates tightly with Kubeflow ecosystem

**Real-world choice:** Use Argo if your team is DevOps-heavy. Use KFP if your team is data-science-heavy.

---

**Next:** [03 -- Model Compression →](03-model-compression.md)
