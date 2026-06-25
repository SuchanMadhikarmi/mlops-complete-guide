# 02 -- Model Types

> You need to know what each model type costs to serve, how it fails, and what infrastructure it needs.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ What machine learning models are (read `01-how-models-learn.md`)
- ✅ Basic model training concepts
- ✅ Python class syntax (for code examples)
- ❓ GPU and CPU concepts
- ❌ NOT required: Deep understanding of each algorithm

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

**What this means:** Each neuron is like a small decision-maker. Many layers stacked together can learn complex patterns. But there's a critical production gotcha:

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
# Dropout randomly disables neurons during training to prevent overfitting
# This randomness is good for learning but BAD for serving
output = model(X)

# Serving -- ALWAYS:
model.eval()     # dropout DISABLED -- deterministic predictions
# Now predictions are consistent. Same input = same output every time.
with torch.no_grad():  # Don't compute gradients (we're not training)
    output = model(X)

# Why no_grad()? Training tracks all computations to calculate gradients.
# For serving, we don't need gradients, so this saves 2x memory and 2x speed.
```

**What breaks if you skip this:**
- Forget `model.eval()`: Dropout is active → same fraud transaction gets different scores on each prediction (catastrophic)
- Forget `torch.no_grad()`: Model is slow and uses 2x memory, pod might run out of memory

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
