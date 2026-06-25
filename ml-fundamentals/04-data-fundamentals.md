# 04 -- Data Fundamentals

> 80% of production ML failures originate in the data pipeline. Leakage, bad splits, imbalance, and training-serving skew cause more incidents than any model bug.

---

## Data Leakage -- The Silent Killer

Model has access to information during training that won't exist at prediction time.

| Type | Example | Detection |
|---|---|---|
| Future information | Using `loan_outcome` to predict loan default | Impossibly good metrics (99%+) |
| Target in features | Using `fraud_confirmed` to predict fraud | Near-perfect accuracy |
| Preprocessing leakage | Normalizing on full dataset before split | Works in dev, fails in prod |
| Group leakage | Same patient in both train and test | Good on test, bad on new entities |

```python
# WRONG: preprocessing leakage
X_scaled = scaler.fit_transform(X)  # ← fit LEARNS the mean/std from test data too!
X_train, X_test = train_test_split(X_scaled)
# Problem: The scaler saw ALL data (including test data) when learning normalization
# Result: Test metrics look better than they should. Reality check: deployment fails.

# RIGHT: fit only on training data
X_train, X_test = train_test_split(X)  # split FIRST
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # learn from train only
X_test_scaled  = scaler.transform(X_test)        # apply learned params to test
# This is realistic: in production, you'll receive NEW data you've never seen
# So normalize using only what you learned from training data

# Save the scaler so serving uses identical normalization
joblib.dump(scaler, 'artifacts/scaler.joblib')
```

**Why this matters:**
- If you fit scaler on full dataset: test metrics are 2-5% too optimistic
- In production: real performance is 2-5% worse than expected
- Silent failure: metrics look good, but business loses money

---

## Train / Validation / Test Split

```
Your dataset:
├── Training (70%)    → Model learns from this
├── Validation (15%)  → Tune hyperparameters, early stopping
└── Test (15%)        → Touch ONCE at the very end. Sacred. Never again.
```

**For time-series: NEVER shuffle randomly.**

```python
# WRONG: future data leaks into training
train, test = train_test_split(time_series_df, shuffle=True)
# Problem: Shuffling mixes past and future randomly
# Example: training sees transactions from Jan AND Dec
# Then model predicts from January using patterns it learned from December (future!)
# Result: "accuracy" 95% in backtest, 60% in production

# RIGHT: chronological split
df = df.sort_values('timestamp')
split = int(len(df) * 0.8)
train = df.iloc[:split]   # Jan-Aug (past)
test  = df.iloc[split:]   # Sep-Dec (future) ← realistic: you can't see the future
# This is realistic: deploy model trained on Jan-Aug, test on Sep-Dec (what will happen)
```

**Why this matters:**
- Time-series with random split: 20-30% metric inflation
- In production: model degrades because it learned from future data
- Detection: compare metrics vs real deployment performance (will differ widely)

---

## Handling Class Imbalance

```python
# Option 1: Class weighting (simplest and most common)
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier()
# sample_weight='balanced' automatically gives higher weight to minority class
# Effect: Model cares more about getting fraud right, less about perfect accuracy on legitimate
model.fit(X_train, y_train, sample_weight=compute_sample_weight('balanced', y_train))

# Option 2: SMOTE (synthetic oversampling) - generates fake minority samples
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
# Now training set has 50/50 fraud/legitimate (balanced)
# Problem: only apply to training data!
# NEVER apply SMOTE to validation or test set - they stay imbalanced (realistic)

# Option 3: Threshold tuning - adjust decision boundary after training
from sklearn.metrics import precision_recall_curve
precision, recall, thresholds = precision_recall_curve(y_val, y_proba)
# Default threshold is 0.5. But for fraud, maybe 0.3 is better (catch more fraud)
f1_scores = 2 * precision * recall / (precision + recall + 1e-8)
best_threshold = thresholds[f1_scores.argmax()]
# Usage: is_fraud = y_proba > best_threshold  (instead of > 0.5)
```

**When to use each:**
- Class weighting: Simplest, always try first
- SMOTE: Works well with tree models, more complex
- Threshold tuning: Best when you need to balance precision vs recall

---

## Feature Engineering Essentials

```python
# Numerical: standardization (always on training data only)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)    # same params, don't refit
joblib.dump(scaler, 'artifacts/scaler.joblib')  # save for serving!

# Log transform for skewed features (e.g. transaction amounts)
df['amount_log'] = np.log1p(df['amount'])    # log(1+x), handles zeros

# Categorical: one-hot for low cardinality (<50 unique values)
df = pd.get_dummies(df, columns=['merchant_category'])

# Missing values: save imputer for serving
imputer = SimpleImputer(strategy='median')
imputer.fit(X_train)
joblib.dump(imputer, 'artifacts/imputer.joblib')  # must match serving!
```

---

## Training-Serving Skew Prevention

```python
# Always normalize timestamps to UTC before computing time features
df['timestamp_utc'] = pd.to_datetime(df['timestamp'], utc=True)
df['hour_utc'] = df['timestamp_utc'].dt.hour   # consistent in training AND serving
# Why UTC? Servers in different timezones would compute different hours otherwise
# 3pm PST != 3pm UTC, so always convert to UTC for reproducibility

# Package preprocessing WITH the model
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),  # handles missing values
    ('scaler', StandardScaler()),                   # normalizes to mean=0, std=1
    ('model', GradientBoostingClassifier())         # the actual model
])
pipeline.fit(X_train, y_train)

# Why pipe? When serving, just do pipeline.predict(X_raw)
# Pipeline automatically: imputes -> scales -> predicts
# Same transformation parameters used training AND serving = no skew
# Without pipeline: You must remember ALL preprocessing steps correctly in serving code

joblib.dump(pipeline, 'artifacts/full_pipeline.joblib')
```

**Real incident from skew:**
- Training: normalized using mean=100, std=20 (learned from data)
- Serving: normalized using mean=102, std=21 (different because forgot to save scaler)
- Result: Model receives inputs in different range than trained on
- Outcome: Accuracy drops 8%, business decision-making suffers

---

**Next:** [Core MLOps → Experiment Tracking](../core-mlops/01-experiment-tracking.md)
