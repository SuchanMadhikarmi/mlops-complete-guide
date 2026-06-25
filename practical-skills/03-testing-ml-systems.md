# 03 -- Testing ML Systems

> ML testing is fundamentally different from software testing. You test data quality, model behavior, pipeline correctness, and regression against production.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ pytest or unittest basics
- ✅ What test fixtures are
- ✅ Model accuracy metrics
- ❓ CI/CD pipeline concepts (read `../core-mlops/04-cicd-for-ml.md`)
- ❌ NOT required: Advanced test frameworks

---

## Why ML Testing Differs from Software Testing

```
Level 1: Data Tests          → validate data before model sees it
Level 2: Model Tests         → validate model behavior
Level 3: Pipeline Tests      → validate end-to-end workflows
Level 4: Regression Gate     → challenger must beat champion
```

---

## Level 1 -- Data Tests

```python
# tests/test_data.py
import pandas as pd
import numpy as np
import pytest

@pytest.fixture
def training_data():
    return pd.read_parquet("data/training_data.parquet")

def test_no_nulls_in_critical_columns(training_data):
    critical = ["user_id", "transaction_id", "amount", "is_fraud"]
    for col in critical:
        assert training_data[col].isnull().sum() == 0, f"Nulls found in {col}"

def test_amount_is_positive(training_data):
    assert (training_data["amount"] > 0).all(), "Non-positive amounts found"

def test_no_duplicate_transactions(training_data):
    dup_count = training_data["transaction_id"].duplicated().sum()
    assert dup_count == 0, f"Found {dup_count} duplicate transaction_ids"

def test_fraud_rate_is_reasonable(training_data):
    fraud_rate = training_data["is_fraud"].mean()
    assert 0.0005 < fraud_rate < 0.3, f"Unusual fraud rate: {fraud_rate:.4%}"

def test_no_future_dates(training_data):
    max_date = training_data["timestamp"].max()
    assert max_date <= pd.Timestamp.now(), f"Future dates found: {max_date}"

def test_minimum_training_samples(training_data):
    assert len(training_data) >= 10_000, f"Too few samples: {len(training_data)}"
```

---

## Level 2 -- Model Tests

```python
# tests/test_model.py
import numpy as np
import pytest
from src.model import load_model, create_test_input

@pytest.fixture
def model():
    return load_model("models/fraud_detector_latest.pkl")

def test_predictions_are_valid_probabilities(model):
    X = create_test_input(n_samples=1000)
    preds = model.predict_proba(X)[:, 1]
    assert preds.min() >= 0.0, "Negative probabilities!"
    assert preds.max() <= 1.0, "Probabilities > 1!"
    assert not np.isnan(preds).any(), "NaN predictions!"
    assert not np.isinf(preds).any(), "Infinite predictions!"

def test_model_is_deterministic(model):
    X = create_test_input(n_samples=10)
    pred1 = model.predict_proba(X)
    pred2 = model.predict_proba(X)
    np.testing.assert_array_almost_equal(pred1, pred2, decimal=6)

def test_model_handles_all_null_optional_fields(model):
    X = create_test_input_with_nulls()   # optional fields set to NaN
    preds = model.predict_proba(X)       # should not crash
    assert not np.isnan(preds).any()

def test_high_risk_scores_higher_than_low_risk(model):
    safe = create_input(amount=50, is_foreign=False, hour=14, credit_score=800)
    risky = create_input(amount=50000, is_foreign=True, hour=3, credit_score=400)
    safe_prob = model.predict_proba(safe)[0, 1]
    risky_prob = model.predict_proba(risky)[0, 1]
    assert risky_prob > safe_prob, (
        f"Model doesn't make sense: risky={risky_prob:.3f} < safe={safe_prob:.3f}"
    )

def test_model_prediction_speed(model):
    import time
    X = create_test_input(n_samples=100)
    start = time.time()
    model.predict_proba(X)
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 100, f"Batch of 100 took {elapsed_ms:.0f}ms (limit: 100ms)"
```

---

## Level 3 -- Pipeline Tests

```python
# tests/test_pipeline.py
import pytest
from src.pipeline import run_training_pipeline

def test_training_pipeline_runs_end_to_end(tmp_path):
    # Test full pipeline on tiny dataset -- should complete without errors.
    # Create minimal test data
    create_test_dataset(n_rows=500, output_path=tmp_path / "test_data.parquet")

    result = run_training_pipeline(
        data_path=str(tmp_path / "test_data.parquet"),
        output_path=str(tmp_path / "model"),
        max_epochs=2,           # don't need full training
        experiment_name="test"  # use test experiment
    )

    assert result.status == "SUCCESS"
    assert (tmp_path / "model").exists()
    assert result.mlflow_run_id is not None

def test_serving_api_validates_input():
    from fastapi.testclient import TestClient
    from src.serve import app

    client = TestClient(app)

    # Missing required field
    response = client.post("/predict", json={"user_id": "u1"})
    assert response.status_code == 422    # validation error, not 500

    # Wrong type
    response = client.post("/predict", json={"user_id": "u1", "amount": "not_a_number"})
    assert response.status_code == 422

    # Valid request
    valid = {"user_id": "u1", "amount": 150.0, "is_foreign": False, "hour_of_day": 14}
    response = client.post("/predict", json=valid)
    assert response.status_code == 200
    data = response.json()
    assert "fraud_probability" in data
    assert 0 <= data["fraud_probability"] <= 1
```

---

## Level 4 -- Deployment Gate (Most Important)

```python
# tests/test_deployment_gate.py -- runs in CI before every deployment
import mlflow
import pytest
from sklearn.metrics import roc_auc_score
import time

def test_challenger_beats_champion():
    # DEPLOYMENT GATE: challenger must not be significantly worse than champion.
    champion   = mlflow.sklearn.load_model("models:/fraud_detector/Production")
    challenger = mlflow.sklearn.load_model("models:/fraud_detector/Staging")

    X_test, y_test = load_held_out_test_set()  # always the same test set

    champion_auc   = roc_auc_score(y_test, champion.predict_proba(X_test)[:,1])
    challenger_auc = roc_auc_score(y_test, challenger.predict_proba(X_test)[:,1])

    print(f"Champion:   AUC={champion_auc:.4f}")
    print(f"Challenger: AUC={challenger_auc:.4f}")

    assert challenger_auc >= champion_auc - 0.005, (
        f"Challenger ({challenger_auc:.4f}) significantly worse than "
        f"champion ({champion_auc:.4f}). Blocking deployment."
    )

def test_challenger_latency_acceptable():
    # New model can't be 50% slower than champion.
    champion   = mlflow.sklearn.load_model("models:/fraud_detector/Production")
    challenger = mlflow.sklearn.load_model("models:/fraud_detector/Staging")

    X_sample = load_held_out_test_set()[0][:100]

    start = time.time(); champion.predict_proba(X_sample)
    champion_ms = (time.time() - start) * 1000

    start = time.time(); challenger.predict_proba(X_sample)
    challenger_ms = (time.time() - start) * 1000

    assert challenger_ms < champion_ms * 1.5, (
        f"Challenger {challenger_ms:.0f}ms vs champion {champion_ms:.0f}ms "
        f"({challenger_ms/champion_ms:.1f}× slower). Blocking deployment."
    )
```

---

**Next:** [04 -- Debugging ML →](04-debugging-ml.md)
