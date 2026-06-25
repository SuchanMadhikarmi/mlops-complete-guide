# 03 -- Evaluation Metrics

> Every metric answers one specific question. Choosing the wrong metric optimizes for the wrong thing.

---

## The Golden Rule

**Never use accuracy for imbalanced datasets.**

```
Fraud dataset: 9,990 legitimate, 10 fraud (0.1%)
Model always predicts "not fraud"
Accuracy = 9,990 / 10,000 = 99.9% ← Looks perfect. Catches ZERO fraud.
```

---

## Classification Metrics

### The Confusion Matrix

```
                Predicted: NOT FRAUD    Predicted: FRAUD
Actual: NOT FRAUD   True Negative (TN)    False Positive (FP) ← False alarm
Actual: FRAUD       False Negative (FN)   True Positive (TP)  ← Caught fraud
                    ↑ Missed fraud
```

### Precision vs Recall Trade-off

| Metric | Formula | Question | Low value means... |
|---|---|---|---|
| Precision | TP / (TP + FP) | When we say FRAUD, are we right? | Too many false alarms |
| Recall | TP / (TP + FN) | Do we catch all actual fraud? | Missing real fraud |
| F1 | 2×(P×R)/(P+R) | Balanced view of both | Both P and R bad |
| ROC-AUC | Area under ROC | Fundamental discrimination ability | Poor ranking |
| PR-AUC | Area under PR curve | Same but for imbalanced data | Use over ROC-AUC when imbalanced |

### Choosing Between Precision and Recall

| Scenario | Prioritize | Why |
|---|---|---|
| Medical screening | **Recall** | Missing disease is dangerous |
| Spam filter | **Precision** | Blocking real email is worse |
| Fraud (bank liability) | **Recall** | Missing fraud costs money |
| Fraud (customer experience) | **Precision** | Blocking legit customers is bad |

---

## Regression Metrics

| Metric | Formula | Outlier Sensitivity | Use When |
|---|---|---|---|
| MAE | avg(|actual - pred|) | Low | All errors equally bad |
| RMSE | √avg((actual-pred)²) | High | Large errors are especially costly |
| MAPE | avg(|actual-pred|/actual)% | Very High | Need scale-independent comparison |
| R² | 1 - SS_res/SS_tot | Medium | Comparing models on same dataset |

---

## Metric Selection Framework

```
Output type?
├── Binary (yes/no)
│   ├── Imbalanced? → PR-AUC + F-beta
│   └── Balanced?   → ROC-AUC + F1
├── Multi-class     → Per-class F1 + macro/weighted average
├── Number          → RMSE (large errors costly) or MAE (equal cost)
└── Ranking         → NDCG@K (full list) or MRR (first result)
```

---

## Calibration -- Are Probabilities Trustworthy?

A model says 70% fraud probability. Does fraud actually happen 70% of the time for those predictions?

```python
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

# Plot reliability diagram
prob_true, prob_pred = calibration_curve(y_test, y_scores, n_bins=10)

# Calibration curve shows: does predicted probability = actual probability?
# Example:
#   For predictions where model said "80% fraud"
#   Did fraud actually occur 80% of the time? Or 50%? Or 95%?

# Perfect calibration = diagonal line from (0,0) to (1,1)
# Points above diagonal = underconfident (model too cautious)
# Points below diagonal = overconfident (model too bold)

# Why it matters:
#   Uncalibrated model prediction of "80% fraud" could actually be 60% or 95%
#   In production: thresholds become wrong
#   Result: Too many false positives or too many missed frauds

# Fix with Platt scaling:
from sklearn.calibration import CalibratedClassifierCV
calibrated = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)
# Sigmoid method learns a transformation: raw_score -> calibrated_probability
calibrated.fit(X_val, y_val)  # fit on validation set (not training!)
# Now predictions are trustworthy
```

**When to check calibration:**
- Any classification model before deployment
- Always on validation data (not training data)

---

**Next:** [04 -- Data Fundamentals →](04-data-fundamentals.md)
