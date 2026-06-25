# 01 -- How Models Actually Learn

> Every model -- from simple fraud detection to GPT-4 -- follows the same 4-step loop. Understand this deeply and you can debug any training failure.

---

## 📚 Who This Is For

This guide is for engineers who know how software works but are new to machine learning. We'll explain what a model is, how it learns, and — most importantly — what breaks in production when you don't understand this.

If you're a DevOps engineer: the key production implication in this guide is `model.eval()` and `torch.no_grad()`. If you remember nothing else, remember those.

---

## What is a Machine Learning Model?

A model is a mathematical function with adjustable parameters (called **weights**). You give it inputs, it produces outputs.

```
Input: [transaction_amount=150, is_foreign=True, hour=3am, credit_score=720]
   ↓
Model (a function with ~10,000 numbers inside called weights)
   ↓
Output: fraud_probability = 0.87
```

The interesting part: **you don't write the logic.** You give the model thousands of examples of inputs + correct outputs (training data), and a learning algorithm adjusts the weights automatically until the function produces correct outputs.

This is fundamentally different from software: in software, you write the rules. In ML, you show the model examples and it figures out the rules itself.

---

## The Training Loop

```
Step 1: Make Prediction  →  Step 2: Measure Error (Loss)
                                          ↓
Step 4: Update Weights   ←  Step 3: Compute Gradient Direction

Repeat millions of times → model learns
```

### Step 1 -- Prediction
Model takes input features, produces an output. Initially random -- knows nothing.

### Step 2 -- Loss (How Wrong Are We?)
A mathematical function measures the gap between prediction and correct answer.

| Loss Function | Task | Key Property |
|---|---|---|
| Binary Cross-Entropy | Binary classification | Penalizes confident wrong predictions |
| Categorical Cross-Entropy | Multi-class | One-vs-all |
| MSE | Regression | Squares errors -- large errors penalized more |
| Focal Loss | Imbalanced classification | Focuses on hard examples |

**Plain English:** Loss is a single number that says "how wrong is the model right now?" Training tries to make this number as small as possible. Low loss = model is good.

### Step 3 -- Gradient (Which Direction?)
Backpropagation calculates: "For each weight, if I increase it slightly, does loss go up or down?"

**Intuition for gradients:** Imagine you're blindfolded on a hilly landscape and you want to reach the lowest valley (lowest loss). You can feel the slope beneath your feet. The gradient tells you: "the ground slopes up in this direction." You take a small step in the opposite direction (downhill). Repeat millions of times. Eventually you reach the valley.

The mathematical term for this process is **gradient descent** — descent toward lower loss by following the gradient downhill.

### Step 4 -- Update Weights
```
new_weight = old_weight - learning_rate × gradient
```

**`learning_rate`** controls the step size. Too large = overshoot the valley and bounce around. Too small = takes forever to reach the valley. This is the single most important hyperparameter to get right.

---

## The Learning Rate

```
Too HIGH:  Loss bounces wildly → never converges
Too LOW:   Training takes forever / never finishes
Just RIGHT: Smooth decrease → good solution
```

**MLOps signal:** "Training isn't converging" → check learning rate first.

---

## Batch Size -- GPU Memory: Why It Matters Operationally

**Batch size** = how many training examples are processed together before updating weights.

Every training example needs GPU memory for:
- The input data itself
- The model's internal calculations (activations)
- The gradients (used to update weights)

Batch of 32 = roughly 32× more memory than batch of 1.

**GPU memory is fixed:**
- NVIDIA T4 (common cloud GPU): 16GB
- NVIDIA A100 (expensive): 80GB

```python
# Batch size controls GPU memory consumption directly
batch_size = 32    # baseline memory usage
batch_size = 64    # ~2x memory
batch_size = 128   # ~4x memory

# OOM (Out of Memory) error fix: reduce batch size by half
# Slow training fix: increase batch size (also scale up learning rate proportionally)
```

The most common error new ML engineers hit: `RuntimeError: CUDA out of memory`. First fix to try: halve the batch size.

---

## Why Random Seeds Matter (Reproducibility)

Models start with **random weights**. Different random initialization can lead to different final models, even with identical code and data.

A **random seed** is a number that fixes the random number generator, making randomness reproducible:

```python
import torch, numpy, random
torch.manual_seed(42)
numpy.random.seed(42)
random.seed(42)
# Now all randomness is deterministic -- same seed = same model
```

**Why this matters for MLOps:**
- **Debugging:** "Is this model worse because of a code bug, or just a different random initialization?" Without a fixed seed, you can't tell.
- **Comparison:** Comparing two training runs only makes sense if the difference between them is the thing you changed (hyperparameter, data), not random chance.
- **Reproducibility:** Recreating the exact production model requires logging the random seed used during training.

**Always log the random seed in your MLflow run.** It's one line and it enables reproducibility.

---

## Critical Production Rules

```python
# Rule 1: ALWAYS call model.eval() before inference
model.eval()                        # disables dropout → deterministic predictions
with torch.no_grad():               # saves memory, faster
    prediction = model(input)

# Forgetting model.eval() = dropout stays active = different prediction every call

# Rule 2: Log 5 things in every training run
mlflow.log_params({
    "git_commit":    get_git_hash(),      # code version
    "data_version":  get_dvc_hash(),      # data version
    "random_seed":   42,                  # random seed
    "docker_image":  "training:v3",       # environment
})
mlflow.log_params(model.get_params())     # ALL hyperparameters
```

---

## Training Failure Diagnosis

| Symptom | First Cause to Check | Fix |
|---|---|---|
| Loss = NaN | LR too high or NaN in data | Reduce LR 10x, validate data |
| Loss not decreasing | LR too low | Increase LR |
| Val loss >> train loss | Overfitting | More data, regularization, early stop |
| Both losses high | Underfitting | More complex model, better features |
| Non-deterministic predictions | `model.eval()` not called | Add `model.eval()` before serving |
| Loss spikes suddenly | Learning rate too high | Add gradient clipping |

---

**Next:** [02 -- Model Types →](02-model-types.md)
