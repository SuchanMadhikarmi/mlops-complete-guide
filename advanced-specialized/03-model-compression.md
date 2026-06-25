# 03 -- Model Compression & Optimization

## Prerequisites

**Core ML knowledge:** Understand what floating point precision is, basic neural network training, inference latency vs accuracy tradeoffs.

**Required tools:** Python 3.8+ · PyTorch or TensorFlow · ONNX · Basic profiling (timing code)

**DevOps context:** Know what it means to reduce resource usage. This directly impacts your cloud bill and latency SLAs.

> A model optimized 3× costs 66% less to serve. For a $10,000/month endpoint, one week of compression work saves $79,920/year.

## Why This Matters (DevOps Translation)

Model compression is like database query optimization:

- **Without optimization:** Query takes 2 seconds, needs 32GB memory. Expensive hardware.
- **With optimization:** Same query takes 200ms, needs 1GB memory. Cheap hardware.

For ML:
- **Without compression:** 7B parameter LLM needs 28GB VRAM. Requires GPU clusters. $5,000+/month.
- **With compression:** Same LLM needs 3.5GB VRAM. Runs on a single GPU. $500/month.

The techniques here are where **real MLOps value lives** -- not building systems, but optimizing deployed systems to reduce cost while maintaining performance.

---

## Quantization -- Reduce Numerical Precision

Weights stored as FP32 (4 bytes) → INT8 (1 byte) = 4× smaller, 4× faster on supported hardware.

| Precision | Bytes/Parameter | 7B Model | Quality Loss |
|---|---|---|---|
| FP32 | 4 | 28 GB | None (baseline) |
| FP16 / BF16 | 2 | 14 GB | Minimal |
| INT8 | 1 | 7 GB | Small |
| INT4 / NF4 | 0.5 | 3.5 GB | Moderate |

### Post-Training Quantization (PTQ) -- No Retraining

```python
from transformers import AutoModelForSequenceClassification
from optimum.onnxruntime import ORTModelForSequenceClassification
from optimum.onnxruntime.configuration import AutoQuantizationConfig

# Load and quantize in one step
quantization_config = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False)

quantizer = ORTQuantizer.from_pretrained("bert-base-uncased-finetuned-fraud")
quantizer.quantize(
    save_dir="bert-fraud-int8",
    quantization_config=quantization_config
)

# Load quantized model for serving -- 4× smaller, 3× faster
model = ORTModelForSequenceClassification.from_pretrained("bert-fraud-int8")
```

**Code walkthrough:** The quantizer automatically reduces each weight from FP32→INT8. This is lossless for the model's behavior because INT8 is sufficient precision for inference (unlike training, which needs FP32).

### Quantization-Aware Training (QAT) -- Retrain for Better Quality

```python
import torch
from torch.quantization import prepare_qat, convert

model = FraudDetector()

# Simulate quantization during training -- model learns to be robust to it
model.train()
model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
model_prepared = prepare_qat(model)

# Train normally -- quantization simulation is automatic
for epoch in range(10):
    for batch in train_loader:
        loss = criterion(model_prepared(batch["features"]), batch["labels"])
        loss.backward()
        optimizer.step()

# Convert to actual quantized model
model_prepared.eval()
model_int8 = convert(model_prepared)
torch.save(model_int8.state_dict(), "model_int8.pt")
```

**Why QAT over PTQ?** PTQ is fast (1 minute) but loses quality. QAT takes longer but the model learns during training that it will be quantized, so when it IS quantized, accuracy stays high.

---

## ONNX -- Universal Serving Format

Train in any framework. Serve with ONNX Runtime -- faster, no framework dependency.

```python
import torch

# Export PyTorch model to ONNX
model.eval()
dummy_input = torch.randn(1, 20)  # 20 input features

torch.onnx.export(
    model,
    dummy_input,
    "fraud_detector.onnx",
    input_names=["features"],
    output_names=["fraud_probability"],
    dynamic_axes={"features": {0: "batch_size"}, "fraud_probability": {0: "batch_size"}},
    opset_version=17
)

# Serve with ONNX Runtime -- no PyTorch needed at serving time
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession(
    "fraud_detector.onnx",
    providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
)

# Inference
features = np.array([[...]], dtype=np.float32)
result = session.run(["fraud_probability"], {"features": features})
probability = float(result[0][0])
```

**Production benefit:** PyTorch at serving = 2GB overhead. ONNX Runtime = 100MB overhead. Saves $50-100/month per model.

---

## TensorRT -- Maximum GPU Performance

Convert ONNX to TensorRT for 3-10× speedup on NVIDIA GPUs.

```bash
# Convert ONNX to TensorRT engine
trtexec --onnx=fraud_detector.onnx \
    --saveEngine=fraud_detector.trt \
    --fp16 \
    --minShapes=features:1x20 \
    --optShapes=features:32x20 \
    --maxShapes=features:128x20
```

**What's happening:** TensorRT analyzes your model, fuses operations together (multiple ops become one), optimizes memory layout. Result: the same computation runs 3-10x faster on GPU.

---

## Knowledge Distillation

Train a small "student" model to mimic a large "teacher" model.

```python
import torch.nn.functional as F

teacher = load_large_model()  # 70B parameters -- accurate but slow
student = SmallModel()        # 7B parameters -- fast

teacher.eval()
for batch in train_loader:
    # Teacher's soft predictions -- contain richer information than hard labels
    with torch.no_grad():
        teacher_logits = teacher(batch["features"])

    # Student learns from teacher's soft probabilities (not just hard labels)
    student_logits = student(batch["features"])

    # Distillation loss: match teacher's probability distribution
    T = 4.0  # temperature -- higher = softer distributions
    distillation_loss = F.kl_div(
        F.log_softmax(student_logits / T, dim=1),
        F.softmax(teacher_logits / T, dim=1),
        reduction="batchmean"
    ) * (T ** 2)

    # Hard label loss: also learn from ground truth
    hard_loss = F.cross_entropy(student_logits, batch["labels"])

    # Combine: 70% distillation, 30% hard labels
    loss = 0.7 * distillation_loss + 0.3 * hard_loss
    loss.backward()
    optimizer.step()
```

**Why this works:** The teacher model learned patterns that matter for the task. By training the student to mimic the teacher, the student learns the same patterns but with fewer parameters.

---

## The Production Optimization Pipeline

```
1. Baseline: train model in PyTorch (FP32)
             measure: latency=200ms, memory=4GB, throughput=50 req/s

2. Export to ONNX
             measure: latency=80ms, memory=3.5GB, throughput=120 req/s

3. Quantize (INT8 PTQ)
             measure: latency=40ms, memory=1GB, throughput=280 req/s

4. Compile to TensorRT (FP16)
             measure: latency=20ms, memory=900MB, throughput=600 req/s

5. Add dynamic batching (Triton)
             measure: throughput=3,000+ req/s

Total improvement: 10× lower latency, 80% cost reduction
```

**Real-world impact:** A team that optimized their fraud detection model saved $2.4M/year in serving costs, while actually improving latency.

---

**Next:** [04 -- Multi-Model Serving (Triton) →](04-multi-model-serving.md)
