# 01 — Statistics for MLOps Engineers

## Prerequisites

**Math background:** Basic understanding of mean, standard deviation, percentiles. Can read a histogram. Don't need calculus.

**ML context:** Have trained models and evaluated them. Understand accuracy, precision, recall, AUC.

**Practical requirement:** Comfortable running Python code, reading outputs.

> You use statistics every single day in MLOps — setting drift thresholds, designing A/B tests, deciding if a new model is actually better. This guide covers exactly what you need.

## Why This Matters (The Data-Driven Culture)

Companies that make decisions based on hunches and intuition fail. Companies that make decisions based on data succeed. Statistics is the language of data-driven decision making in ML.

- "Is this model actually better?" → statistics
- "Has input data drifted significantly?" → statistics  
- "Is this A/B test result real or just randomness?" → statistics

Learning statistics makes you invaluable because you can answer these questions rigorously.

---

## Distributions — What Your Data Looks Like

A distribution describes what values your data takes and how often each value appears.

### Normal Distribution (Bell Curve)

Most values cluster around the center. Fewer values as you move toward extremes. The most common pattern in nature and in ML feature distributions.

```
Mean (center): where most values cluster
Std Dev:       how spread out the values are

68% of values fall within 1 std dev of the mean
95% of values fall within 2 std devs
99.7% of values fall within 3 std devs

"3-sigma alert" = value more than 3 std devs from mean → very unusual
```

### Why Distributions Matter for MLOps

```python
import pandas as pd
import numpy as np

# Monitor feature distributions over time
def compute_distribution_stats(series: pd.Series) -> dict:
    return {
        "mean": float(series.mean()),
        "std": float(series.std()),
        "min": float(series.min()),
        "p25": float(series.quantile(0.25)),
        "p50": float(series.median()),
        "p75": float(series.quantile(0.75)),
        "p95": float(series.quantile(0.95)),
        "p99": float(series.quantile(0.99)),
        "max": float(series.max()),
        "null_rate": float(series.isnull().mean())
    }

# Run daily, compare to training baseline
# Alert when stats deviate significantly from baseline
```

**Production consequence:** A payment amount feature that shifted from mean=$100 to mean=$10,000 would break a fraud model. Statistical monitoring catches this automatically.

---

## Hypothesis Testing

### The Core Question

"Model B performed 2% better than Model A. Is that real, or just lucky randomness with the traffic it received?"

Hypothesis testing answers this rigorously.

### The Framework

```
Step 1: State null hypothesis
        H₀: "Models A and B perform identically. Any difference is random."

Step 2: Collect data
        Run both models on real traffic

Step 3: Compute test statistic
        How far is the observed difference from zero?

Step 4: Calculate p-value
        If H₀ were true, how likely is this result by chance?

Step 5: Make decision
        p < 0.05 → reject H₀ → "difference is real"
        p ≥ 0.05 → fail to reject H₀ → "not enough evidence"
```

### P-Value Interpretation

```
p = 0.80 → 80% chance this result is just random noise. Ignore it.
p = 0.20 → 20% chance. Still too uncertain.
p = 0.05 → 5% chance. Industry standard threshold — declare significant.
p = 0.01 → 1% chance. High confidence.
p = 0.001 → 0.1% chance. Very strong evidence.

Rule: p < 0.05 = statistically significant
```

### Common Statistical Tests

| Test | Use When | Python |
|---|---|---|
| t-test (independent) | Compare means of two groups | `scipy.stats.ttest_ind` |
| Mann-Whitney U | Non-parametric comparison | `scipy.stats.mannwhitneyu` |
| Chi-squared | Compare categorical distributions | `scipy.stats.chi2_contingency` |
| KS test | Compare two distributions | `scipy.stats.ks_2samp` |
| Z-test for proportions | Compare click rates, fraud rates | `statsmodels.stats.proportion` |

```python
from scipy import stats
import numpy as np

# Example: Are Model A and Model B conversion rates different?
model_a_conversions = 450  # out of 5000 users
model_b_conversions = 520  # out of 5000 users

# Two-proportion z-test
from statsmodels.stats.proportion import proportions_ztest

counts = np.array([model_a_conversions, model_b_conversions])
nobs = np.array([5000, 5000])

z_stat, p_value = proportions_ztest(counts, nobs)
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Statistically significant difference!")
else:
    print("No significant difference detected.")
```

---

## Confidence Intervals

A point estimate (92% accuracy) is not enough. You need the range.

```python
from scipy import stats
import numpy as np

def confidence_interval_for_auc(y_true, y_pred_proba, confidence=0.95, n_bootstrap=1000):
    """Bootstrap confidence interval for AUC"""
    from sklearn.metrics import roc_auc_score
    
    aucs = []
    n = len(y_true)
    
    for _ in range(n_bootstrap):
        indices = np.random.choice(n, n, replace=True)
        auc = roc_auc_score(y_true[indices], y_pred_proba[indices])
        aucs.append(auc)
    
    alpha = 1 - confidence
    lower = np.percentile(aucs, alpha/2 * 100)
    upper = np.percentile(aucs, (1 - alpha/2) * 100)
    
    return lower, upper

lower, upper = confidence_interval_for_auc(y_test, y_pred)
print(f"AUC: {auc:.3f} [{lower:.3f}, {upper:.3f}]")
# AUC: 0.923 [0.911, 0.934]
```

### Overlapping Intervals = No Clear Winner

```
Model A: AUC 0.920 ± 0.015  → [0.905, 0.935]
Model B: AUC 0.930 ± 0.020  → [0.910, 0.950]

These intervals OVERLAP → cannot confidently say B is better
Need more data before declaring a winner.

Model A: AUC 0.920 ± 0.003  → [0.917, 0.923]
Model B: AUC 0.935 ± 0.003  → [0.932, 0.938]

These intervals DON'T overlap → B is genuinely better.
```

---

## PSI — Population Stability Index

The industry-standard metric for detecting when your input data has drifted from training distribution. Used heavily in financial services MLOps.

### How PSI Works

```python
import numpy as np

def compute_psi(expected: np.array, actual: np.array, buckets: int = 10) -> float:
    """
    Compute PSI between expected (training) and actual (production) distributions.
    
    PSI < 0.1:  No significant drift
    PSI < 0.2:  Moderate drift — monitor closely
    PSI >= 0.2: Significant drift — consider retraining
    """
    def _psi(expected_pct, actual_pct):
        # Avoid log(0)
        expected_pct = np.where(expected_pct == 0, 0.0001, expected_pct)
        actual_pct = np.where(actual_pct == 0, 0.0001, actual_pct)
        return (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)
    
    # Bin the data
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]
    
    # Convert to percentages
    expected_pct = expected_counts / len(expected)
    actual_pct = actual_counts / len(actual)
    
    # Compute PSI
    psi_values = _psi(expected_pct, actual_pct)
    return np.sum(psi_values)

# Usage
training_ages = train_df["age"].values
production_ages = last_week_df["age"].values

psi = compute_psi(training_ages, production_ages)
print(f"PSI for age: {psi:.4f}")

if psi > 0.2:
    trigger_retraining_alert("Age feature has significant drift")
```

---

## Statistical Power and Sample Size

### Why Sample Size Matters

```
Scenario: You ran an A/B test for 3 days.
          Model A: 87% accuracy (500 users)
          Model B: 89% accuracy (500 users)
          p-value = 0.18 → "not significant"

You conclude: "No difference."

Reality: You didn't have enough data to detect a 2% difference.
         With 5,000 users per group, p-value would be 0.02 → significant!

This is a Type II error: failing to detect a real difference.
```

### Calculate Required Sample Size

```python
from scipy.stats import norm

def required_sample_size(
    baseline_rate: float,
    min_effect: float,    # minimum improvement you care about
    alpha: float = 0.05,  # significance level
    power: float = 0.80   # probability of detecting real difference
) -> int:
    """Calculate samples needed per group for an A/B test."""
    p1 = baseline_rate
    p2 = baseline_rate + min_effect
    
    z_alpha = norm.ppf(1 - alpha / 2)  # 1.96 for α=0.05
    z_beta = norm.ppf(power)            # 0.84 for 80% power
    
    n = (
        (z_alpha + z_beta) ** 2
        * (p1 * (1 - p1) + p2 * (1 - p2))
        / (p2 - p1) ** 2
    )
    return int(np.ceil(n))

# Example: 5% baseline conversion rate, want to detect 1% improvement
n = required_sample_size(0.05, 0.01)
print(f"Need {n} users per group = {2*n} total")
# Need 3,094 users per group = 6,188 total

# If you get 500 users/day → run test for 13 days minimum
```

---

**Next:** [02 — Data Engineering →](02-data-engineering.md)
