# 01 -- Docker for ML

> ML workloads use Docker differently from standard software. GPU containers, CUDA compatibility, and multi-stage builds are ML-specific skills.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ Docker fundamentals (FROM, RUN, COPY, EXPOSE, docker build, docker run)
- ✅ Multi-stage builds (at least the concept)
- ✅ Docker volumes and bind mounts
- ❓ GPUs and CUDA — fully explained below
- ❌ NOT required: ML or PyTorch experience

---

## Why ML Docker is Different from Regular Docker

You already know Docker. You've containerized web servers, APIs, databases. For those, you pick a base image, copy your code, install dependencies, done.

ML containers add three complications:

**1. GPUs:** Standard Docker cannot access the host GPU. Training a neural network on CPU instead of GPU is 10-100x slower. GPU support requires special setup.

**2. CUDA:** GPU programs use NVIDIA's CUDA toolkit. The CUDA version in your container must match what your ML framework (PyTorch/TensorFlow) expects, and must be compatible with the GPU driver on the host. One version mismatch = GPU completely unavailable.

**3. Image size:** A standard Python app Docker image is 200-500MB. An ML image with PyTorch is 5-15GB. This changes how you think about layer caching, multi-stage builds, and pull times.

This guide addresses all three.

---

## Why GPUs Matter for ML: The Short Version

**CPU:** Has a small number (4-64) of powerful, general-purpose cores. Great for sequential logic, branching, varied tasks.

**GPU:** Has thousands of simple, specialized cores. Terrible for complex logic, but phenomenal for doing the same simple operation on millions of values simultaneously.

ML training is almost entirely matrix multiplication — exactly the kind of massively parallel simple operation GPUs are built for.

```
Training on CPU:   3 weeks for a medium-sized model
Training on GPU:   4 hours for the same model
```

For serving (inference), GPUs also matter: they allow batching many user requests together and processing them in one GPU call, dramatically increasing throughput.

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

---

## CUDA Version Compatibility: Why This Breaks and How to Fix It

CUDA is NVIDIA's platform for GPU programming. PyTorch and TensorFlow are compiled against a specific CUDA version. If the CUDA version in your container doesn't match what PyTorch was compiled for, PyTorch silently falls back to CPU — no GPU, no error message, just slow.

**The version chain:**
```
NVIDIA GPU Driver (on host machine)
    ↓ supports up to CUDA version X
CUDA toolkit (in container)
    ↓ must match what PyTorch was compiled for
PyTorch (in container)
    ↓ uses GPU only if CUDA matches
```

**If any link in the chain is wrong:** PyTorch runs on CPU. You don't find out until training is 50x slower than expected.

**How to debug:**

```bash
# Check on host machine
nvidia-smi | grep "CUDA Version"   # max CUDA the driver supports

# Check inside container
python -c "import torch; print('PyTorch CUDA:', torch.version.cuda)"
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

**Use NVIDIA's pre-built base images -- never install CUDA manually:**

```dockerfile
# Training (full CUDA toolkit + compilers)
FROM nvcr.io/nvidia/pytorch:23.10-py3
# This image has: CUDA toolkit, cuDNN, PyTorch, common ML libraries
# Size: ~10-12GB  |  Use for: Training jobs where you might compile custom operations

# Serving (smaller -- only runtime libraries, no compilers)
FROM nvcr.io/nvidia/cuda:12.2.0-runtime-ubuntu22.04
# This image has: CUDA runtime, cuBLAS, cuDNN (inference-only)
# Size: ~2-3GB    |  Use for: Inference where model is already compiled
```

> **Why two different base images?** Training might need to compile custom CUDA operations (common with newer architectures). Serving only runs pre-compiled model forward passes. The runtime image is 3-5x smaller, meaning faster pod startup and lower egress costs.

---

## Multi-Stage Build -- Keep Images Small

Without multi-stage builds, ML images easily reach 15GB. Here's why that matters for operations:

- **Pod startup time:** Kubernetes pulls the image before starting the pod. A 15GB pull on a node without cache takes 5-10 minutes. A 3GB image takes 1 minute. This directly affects how fast you can scale.
- **Registry costs:** Pushing and pulling 15GB images is expensive in both bandwidth and storage.
- **Attack surface:** Larger images have more installed packages, more potential vulnerabilities.

**Multi-stage build strategy for ML:**
```
Stage 1 (Builder): Start with full PyTorch image (10GB)
  → pip install all dependencies
  → This stage has compilers, build tools, etc.

Stage 2 (Runtime): Start with minimal CUDA runtime image (2GB)
  → COPY only the installed Python packages from stage 1
  → COPY only the application code
  → Final image: ~3-4GB (not 10GB)
```

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

## Layer Caching Strategy: Why Order Matters

Docker builds images layer by layer and caches each layer. A layer is only rebuilt if it or any layer above it has changed. This matters enormously for ML images because dependencies take 3-10 minutes to install.

**The principle: put things that change least at the top.**

```dockerfile
# WRONG order -- one code change rebuilds everything including 5 min pip install
COPY . .
RUN pip install torch transformers fastapi pydantic uvicorn

# RIGHT order -- code changes only rebuild the final layer
FROM python:3.10-slim

# Layer 1: Base image (never changes unless you pin to a new tag)
# Layer 2: System packages (changes rarely -- maybe monthly)
RUN apt-get update && apt-get install -y libgomp1

# Layer 3: Stable ML dependencies (pin versions, changes rarely)
RUN pip install torch==2.1.0 transformers==4.35.0

# Layer 4: App dependencies (changes sometimes)
COPY requirements-app.txt .
RUN pip install -r requirements-app.txt

# Layer 5: Code (changes daily -- but rebuild is instant)
COPY src/ ./src/
```

With this order, when you push a code change:
- Layers 1-4 are served from cache (≈0 seconds)
- Only layer 5 rebuilds (≈2 seconds)
- Total build time: ~5 seconds instead of 8 minutes

> In a development workflow where you're iterating quickly, this 8-minute vs 5-second difference is the difference between productive and miserable.

---

## Model Loading Strategies: When to Use Each

How the model file gets into the container is a key architectural decision. Each option has different trade-offs:

```dockerfile
# Option A: Bake model into image (self-contained, large images)
COPY models/fraud_model_v23.onnx /app/model/
```
**Use when:** Model is < 1GB, updates infrequently (monthly), simplicity matters.
**Problem:** Every model update requires a new Docker build and push. If model is 500MB, every CI/CD run pushes 500MB+ of image layers.

---

```python
# Option B: Download at startup (small image, model from registry)
import mlflow
model = mlflow.sklearn.load_model("models:/fraud_detector/Production")
```
**Use when:** Model is large (1GB+) or updates frequently (weekly/daily).
**Problem:** Cold start time — pod takes 30-60 seconds to download model. Configure `readinessProbe.initialDelaySeconds` to match.

---

```bash
# Option C: Mount as volume (fastest startup, needs infrastructure)
docker run -v /host/models:/app/model fraud-serving:latest
```
**Use when:** Local development only.
**Problem:** Not production-safe — no version tracking, depends on host filesystem, hard to reproduce.

**Production recommendation:** Option B (download from MLflow) for most cases. It keeps images small, enables model updates without rebuilds, and integrates with your model registry.

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
