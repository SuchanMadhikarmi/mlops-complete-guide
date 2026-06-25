# 02 -- Kubernetes for ML

> Your DevOps K8s knowledge applies directly. These are the ML-specific patterns on top.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ Kubernetes basics (deployments, pods, services)
- ✅ kubectl commands
- ✅ Resource requests/limits
- ❓ What GPUs are and why they matter
- ❌ NOT required: GPU-specific K8s plugins

---

## Why K8s for ML is Different

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
