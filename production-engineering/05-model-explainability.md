# 05 -- Model Explainability (SHAP + LIME)

> Explainability is not optional in regulated industries. It's also your best debugging tool for model behavior in production.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ What model predictions are and how they work
- ✅ Feature importance concept
- ✅ Basic Python (numpy, dictionaries)
- ❓ Debugging and troubleshooting
- ❌ NOT required: Game theory, Shapley values (SHAP theory)

---

## Why Explainability Matters in Production

1. **Regulatory compliance** -- GDPR Article 22, EU AI Act, financial regulations require explanations for automated decisions
2. **Debugging** -- When a model makes a surprising prediction, SHAP tells you exactly why
3. **Drift detection** -- Tracking SHAP distributions over time reveals what's changing
4. **Trust** -- Business stakeholders and auditors need to understand what the model is doing

---

## SHAP -- The Gold Standard

SHAP (SHapley Additive exPlanations) answers: **"For this specific prediction, how much did each feature contribute?"**

```python
import shap
import numpy as np

model = load_model("models/fraud_detector.pkl")
X_test = load_test_data()

# TreeExplainer -- for tree models (XGBoost, LightGBM, Random Forest)
# Fast and exact -- use this in production
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
# shap_values shape: (n_samples, n_features)
# Each value: how much that feature pushed the prediction up or down
```

### Local Explanation (One Prediction)

```python
# Explain a single suspicious transaction
sample = X_test.iloc[42:43]
shap_val = explainer.shap_values(sample)[0]

print(f"Base rate (avg fraud probability): {explainer.expected_value:.3f}")
print(f"Final prediction: {model.predict_proba(sample)[0,1]:.3f}")
print()
for feat, sv in zip(feature_names, shap_val):
    direction = "▲" if sv > 0 else "▼"
    print(f"{direction} {feat:30s}: {sv:+.4f}")

# Output:
# Base rate: 0.082
# Final prediction: 0.891
# ▲ amount                        : +0.312  ← high amount pushed fraud prob up
# ▲ is_foreign                    : +0.245  ← foreign transaction adds risk
# ▲ hour_of_day (3am)             : +0.189  ← unusual time
# ▼ account_age_days              : -0.021  ← long-standing account reduces risk
```

### Global Explanation (All Predictions)

```python
# Which features matter most overall?
mean_abs_shap = np.abs(shap_values).mean(axis=0)
feature_importance = dict(zip(feature_names, mean_abs_shap))
sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)

print("Global Feature Importance (mean |SHAP|):")
for feat, importance in sorted_features[:10]:
    bar = "█" * int(importance * 100)
    print(f"{feat:30s} {importance:.4f} {bar}")
```

### SHAP in API Response

```python
@app.post("/predict")
async def predict(request: PredictionRequest):
    features = prepare_features(request)
    prediction = model.predict_proba(features)[0, 1]

    # Include explanation in response (for compliance)
    shap_values = explainer.shap_values(features)[0]
    explanation = {
        feat: round(float(sv), 4)
        for feat, sv in zip(feature_names, shap_values)
        if abs(sv) > 0.01  # only show significant contributors
    }

    return {
        "fraud_probability": round(float(prediction), 4),
        "explanation": explanation,
        "base_rate": round(float(explainer.expected_value), 4)
    }
```

---

## SHAP Explainer Types

| Explainer | Models | Speed | Accuracy |
|---|---|---|---|
| `TreeExplainer` | XGBoost, LightGBM, Random Forest | Fast | Exact |
| `LinearExplainer` | Linear/Logistic Regression | Fast | Exact |
| `DeepExplainer` | Neural Networks (PyTorch/TF) | Medium | Approximate |
| `KernelExplainer` | Any model | Very slow | Approximate |

**Rule:** Use `TreeExplainer` for tree models. Use `KernelExplainer` only as last resort.

---

## LIME -- When to Use Instead

LIME (Local Interpretable Model-agnostic Explanations) creates a local linear approximation around one prediction.

```python
from lime.lime_tabular import LimeTabularExplainer

explainer = LimeTabularExplainer(
    X_train.values,
    feature_names=feature_names,
    class_names=["legitimate", "fraud"],
    mode="classification"
)

explanation = explainer.explain_instance(
    X_test.iloc[42].values,
    model.predict_proba,
    num_features=10
)

# Get feature weights
for feat, weight in explanation.as_list():
    print(f"{feat}: {weight:+.4f}")
```

### SHAP vs LIME

| Factor | SHAP | LIME |
|---|---|---|
| Accuracy | Exact (tree models) | Approximate |
| Consistency | Same result every run | Non-deterministic |
| Speed | Fast for trees | Always slow |
| Best for | Production, compliance | Research, images, text |

**Use SHAP in production. Use LIME for exploration or non-tree models where SHAP is slow.**

---

**Next:** [06 -- Inference Patterns →](06-inference-patterns.md)
