# 01 -- Distributed Training (Ray + DeepSpeed)

> When a model doesn't fit on one GPU or training takes too long on one machine, distributed training is the solution.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ PyTorch basics (models, training loops)
- ✅ CUDA and GPU concepts
- ✅ What gradient descent is
- ❓ Kubernetes or cluster concepts
- ❌ NOT required: MPI or advanced distributed systems

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

**How it works:**
- GPU 0: trains on batch of 1000 samples
- GPU 1: trains on different 1000 samples (simultaneously)
- GPU 2: trains on another 1000 samples (simultaneously)
- After each iteration: Sync gradients (average them across all GPUs)
- Result: 3x speedup (roughly)

```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def train_ddp(rank, world_size):
    # rank = which GPU (0, 1, 2...)
    # world_size = total GPUs (4)
    
    # Setup communication between GPUs
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    # NCCL = NVIDIA's communication library (optimized for GPUs)
    
    torch.cuda.set_device(rank)  # This process uses GPU #rank

    # Each GPU gets its own model copy
    model = FraudDetector().to(rank)
    model = DDP(model, device_ids=[rank])  
    # DDP wraps model, automatically syncs gradients between GPUs

    # Each GPU gets different data (no duplication)
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    # sampler ensures GPU 0 sees rows 0-999, GPU 1 sees 1000-1999, etc
    
    loader = DataLoader(dataset, sampler=sampler, batch_size=64)
    optimizer = torch.optim.Adam(model.parameters())

    for batch in loader:
        optimizer.zero_grad()
        loss = criterion(model(batch["features"]), batch["labels"])
        loss.backward()           
        # Gradients computed locally on this GPU
        # DDP automatically averages gradients across all 4 GPUs
        # All 4 GPUs update their weights identically
        optimizer.step()          

    dist.destroy_process_group()  # cleanup

# Launch on 4 GPUs
torch.multiprocessing.spawn(train_ddp, args=(4,), nprocs=4)
# Starts 4 processes, each using 1 GPU
```

**What breaks if you skip DDP:**
- No syncing between GPUs → each GPU trains its own model differently
- Result: 4 different models, not 1 model trained 4x faster

---

## ZeRO -- Memory Optimization (DeepSpeed)

Standard data parallelism: every GPU holds full model + gradients + optimizer states = 3× redundancy.

ZeRO eliminates redundancy by sharding across GPUs:

**Example: 7B parameter model (28GB in FP32)**
- Normal data parallelism: each GPU needs 28GB × 3 = 84GB
- With 8 GPUs: 84GB / 8 = 10.5GB per GPU (fits on A100)
- ZeRO Stage 3: 28GB / 8 = 3.5GB per GPU (fits on T4!)

| Stage | Shards | Memory Reduction | What Gets Split |
|---|---|---|---|
| ZeRO-1 | Optimizer states only | 4× | Optimizer keeps separate params for each checkpoint |
| ZeRO-2 | Optimizer + Gradients | 8× | Both optimizer and gradients split across GPUs |
| ZeRO-3 | Optimizer + Gradients + Model Parameters | ∝ GPUs | Everything split (most aggressive) |

```python
# deepspeed_config.json
{
    "zero_optimization": {
        "stage": 3,
        # If GPU memory full, offload to CPU RAM (slower but doesn't crash)
        "offload_optimizer": {"device": "cpu"},
        "offload_param": {"device": "cpu"}
    },
    "fp16": {"enabled": true},  # Use 16-bit precision (half memory)
    "train_batch_size": 256
}
```

**Trade-off:**
- ZeRO-1/2: Fast but needs more GPU memory
- ZeRO-3: Slower (more communication) but fits on cheaper GPUs
- Choose based on your hardware

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
