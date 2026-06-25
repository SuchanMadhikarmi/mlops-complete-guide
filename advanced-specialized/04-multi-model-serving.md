# 04 -- Multi-Model Serving (NVIDIA Triton)

## Prerequisites

**From DevOps/Infrastructure perspective:** Understand load balancing, containerization, and horizontal scaling. Familiar with Docker and basic networking.

**From ML perspective:** Have deployed at least one model endpoint. Know what model serving latency means.

**Required tools:** Docker · Kubernetes · Python 3.8+ · Prometheus for metrics

> When you have 10+ models to serve, managing separate containers per model is an operational nightmare. Triton serves all models from a unified platform.

## Why This Matters (DevOps Translation)

Think of Triton like a reverse proxy (Nginx/HAProxy) but for ML models:

- Without Triton: 20 models = 20 Docker containers = 20 resource allocations = 20 deployment pipelines
- With Triton: 20 models = 1 container = unified resource management = single deployment pipeline

This drastically simplifies operations: instead of managing 20 separate services, you manage one Triton instance with multiple models.

---

## Why Triton?

| Approach | Problem |
|---|---|
| One FastAPI container per model | 20 models = 20 deployments, 20 CI/CD pipelines, 20 monitoring setups |
| NVIDIA Triton Inference Server | One server hosts all models, all frameworks, managed automatically |

**Cost impact:** Reduce overhead 20x, save ~$40k/year per cluster on operational complexity.

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

**Production consequence:** With dynamic batching, your GPU costs drop 50% because you're using the GPU more efficiently.

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
