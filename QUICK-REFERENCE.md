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
