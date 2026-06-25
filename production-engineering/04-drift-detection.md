# 04 -- Drift Detection

> Models don't crash when the world changes. They silently give worse answers. Drift monitoring is your early warning system.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ What data drift, concept drift, label drift are (read `02-continuous-training.md`)
- ✅ Basic statistics and distributions
- ✅ Monitoring concepts (alerts, thresholds)
- ❓ Feature importance (read `05-model-explainability.md`)
- ❌ NOT required: PSI calculation details

---

## The 3 Types of Drift

| Type | What Changes | Example | Response |
|---|---|---|---|
| **Data drift** (Covariate shift) | Input distribution P(X) | New user demographic joins | Retrain with representative data |
| **Concept drift** | Relationship P(Y|X) | Fraud patterns fundamentally change | Rethink features, retraining strategy |
| **Label drift** | Target distribution P(Y) | Fraud rate drops from 1% to 0.01% | Adjust class weights, retune threshold |

**Critical:** These require completely different responses. Never treat concept drift as data drift.

---

## PSI -- Population Stability Index

Industry-standard metric for detecting input feature drift.

```python
import numpy as np

def compute_psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts   = np.histogram(actual,   bins=breakpoints)[0]

    expected_pct = np.where(expected_counts == 0, 0.0001, expected_counts / len(expected))
    actual_pct   = np.where(actual_counts   == 0, 0.0001, actual_counts   / len(actual))

    return float(np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct)))

# Thresholds:
# PSI < 0.10  → No significant drift
# PSI < 0.20  → Moderate drift -- monitor closely
# PSI >= 0.20 → Significant drift -- trigger retraining
```

---

## Evidently AI -- Complete Drift Dashboard

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import ColumnDriftMetric, ColumnDistributionMetric

def run_drift_report(reference_df, production_df, output_path="reports/drift.html"):
    report = Report(metrics=[
        DataDriftPreset(),
        DataQualityPreset(),
        ColumnDriftMetric(column_name="transaction_amount"),
        ColumnDriftMetric(column_name="fraud_probability"),  # monitor prediction dist
        ColumnDistributionMetric(column_name="fraud_probability"),
    ])
    report.run(reference_data=reference_df, current_data=production_df)
    report.save_html(output_path)

    result = report.as_dict()
    drift_detected = result["metrics"][0]["result"]["dataset_drift"]
    n_drifted = result["metrics"][0]["result"]["number_of_drifted_columns"]

    if drift_detected:
        trigger_retraining_alert(f"{n_drifted} features drifted -- check {output_path}")

    return result
```

---

## SHAP-Based Drift -- Early Warning

Track SHAP value distributions over time. If a feature's SHAP values shift, that feature is increasingly (or decreasingly) driving predictions -- a more sensitive signal than raw PSI.

```python
import shap
import numpy as np

def monitor_shap_drift(model, X_production, baseline_shap, feature_names):
    explainer = shap.TreeExplainer(model)
    production_shap = explainer.shap_values(X_production)

    baseline_importance   = np.abs(baseline_shap).mean(axis=0)
    production_importance = np.abs(production_shap).mean(axis=0)

    for i, feature in enumerate(feature_names):
        if baseline_importance[i] == 0:
            continue
        relative_change = abs(production_importance[i] - baseline_importance[i]) / baseline_importance[i]
        if relative_change > 0.30:  # >30% change in feature importance
            print(f"SHAP drift on '{feature}': {relative_change:.1%} change in importance")
```

---

## Prediction Distribution Monitoring

The fastest drift signal -- watch for shifts in your model's output distribution.

```python
def monitor_prediction_distribution(current_predictions, baseline_stats):
    current_mean = np.mean(current_predictions)
    current_std  = np.std(current_predictions)

    baseline_mean = baseline_stats["mean"]
    baseline_std  = baseline_stats["std"]

    # Mean shift
    if abs(current_mean - baseline_mean) > 2 * baseline_std:
        alert(f"Prediction mean shifted: {baseline_mean:.3f} → {current_mean:.3f}")

    # Distribution shape change (use KS test)
    from scipy.stats import ks_2samp
    ks_stat, p_value = ks_2samp(baseline_predictions, current_predictions)
    if p_value < 0.01:
        alert(f"Prediction distribution changed significantly (KS p={p_value:.4f})")
```

---

## Drift Response Runbook

```
PSI 0.10-0.20 on any feature:
    → Log and alert team
    → Increase monitoring frequency
    → No automatic retraining yet

PSI > 0.20 on any top-5 feature:
    → Trigger CT pipeline immediately
    → Send Slack alert with PSI scores
    → Begin root cause investigation

PSI > 0.20 on multiple features simultaneously:
    → This may be concept drift, not data drift
    → Do NOT just retrain -- investigate WHY features changed
    → May need new features or new model architecture

Prediction distribution shifts suddenly:
    → Check feature pipeline first (most likely cause)
    → Check if wrong model version was deployed
    → Check for upstream data schema changes
```

---

**Next:** [05 -- Model Explainability →](05-model-explainability.md)
