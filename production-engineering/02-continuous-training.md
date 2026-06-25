# 02 -- Continuous Training (CT) Pipelines

> Continuous Training is ML's equivalent of Continuous Deployment. Models must auto-retrain when the world changes, pass quality gates, and deploy safely.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ CI/CD pipelines (automated triggers, quality gates, deploy steps)
- ✅ Python basics (functions, decorators)
- ✅ Docker and Kubernetes (jobs, CronJobs)
- ❓ MLflow experiment tracking — read `core-mlops/01-experiment-tracking.md` first
- ❌ NOT required: Prefect or Airflow experience (will be explained)

---

## Why Continuous Training Exists: The Problem First

Before understanding the solution, you need to understand the problem: **data drift**.

### What is Data Drift?

Imagine you build a fraud detection model. You train it on all fraud cases from 2024. It learns patterns: fraudsters in 2024 tend to make small test transactions first, then large purchases, primarily at online merchants between 2-4am.

Now it's 2025. Fraudsters adapt. They've changed tactics. Now they target in-store transactions during business hours and don't do test transactions. The fraud patterns have shifted.

Your model was never retrained. It's still looking for 2024 fraud patterns. Your fraud detection rate drops from 89% to 71% — **with zero code changes, zero infrastructure changes, zero errors in your logs.**

This is data drift. The world changed. The model didn't. Performance degrades silently.

> **DevOps analogy:** Imagine if your load balancer health check criteria became wrong over time because the definition of "healthy" changed, but nobody updated the check. Traffic routes to degraded services with no alerts. That's what drift does to ML models.

### What is Concept Drift?

An even harder problem: sometimes the *relationship* between inputs and outputs changes, not just the input distribution.

Example: You build a credit scoring model. During a recession, the historical relationship between income level and default probability changes fundamentally. High earners who were safe before now default more due to job losses in previously stable industries.

Retraining on more recent data helps, but if your *features* (income, employment type) no longer capture the relevant patterns, retraining won't fully fix it. You may need to redesign what the model measures.

**This is why you need 3 different response strategies for 3 different drift types** (covered in `production-engineering/04-drift-detection.md`).

---

## The 3 Retraining Triggers

| Trigger | How it Works | Best For |
|---|---|---|
| **Time-based** | Retrain every N days regardless of performance | Simple, predictable, but may retrain when not needed or miss drift between schedules |
| **Performance-based** | Retrain when accuracy drops below threshold | Gold standard — only retrains when actually needed, but requires ground truth labels to measure accuracy |
| **Drift-based** | Retrain when PSI > 0.2 on key features | Proactive — acts before performance degrades, doesn't need labels, but can false-positive |

> **PSI (Population Stability Index)** is a number that measures how much a data distribution has changed. PSI < 0.1: stable. PSI 0.1-0.2: monitor. PSI > 0.2: significant shift, trigger action. It's essentially a "how different is this data from training data?" score.

---

## The 7-Step CT Pipeline: What Each Step Does

```
[1] Data Validation      → Great Expectations checks. Abort if data is bad.
         ↓
[2] Feature Engineering  → Use same definitions as serving (feature store)
         ↓
[3] Model Training       → All params, seeds, data version logged to MLflow
         ↓
[4] Evaluation Gate      → Challenger must beat champion -- block if not
         ↓
[5] Model Registration   → Push to MLflow registry as "Staging"
         ↓
[6] Deployment           → Auto (low risk) or manual approval (high risk)
         ↓
[7] Post-Deploy Watch    → Monitor 24-72h → auto-rollback if degraded
```
The 7-step pipeline below answers: "what happens between 'new training data is available' and 'new model is live in production'?" Each step is a quality gate.

```
[1] Data Validation      → Great Expectations checks. Abort if data is bad.
         ↓
         Why: Garbage in = garbage out. A model trained on bad data will be worse
              than the current model. Step 1 catches this before wasting hours training.
[2] Feature Engineering  → Use same definitions as serving (feature store)
         ↓
         Why: Features must be computed identically in training and serving.
              Differences cause training-serving skew — silent accuracy degradation.
[3] Model Training       → All params, seeds, data version logged to MLflow
         ↓
         Why: Must be reproducible. Log everything.
[4] Evaluation Gate      → Challenger must beat champion -- block if not
         ↓
         Why: New model might be worse due to overfitting, bad data slice, or bad random
              seed. Never auto-deploy without this gate.
[5] Model Registration   → Push to MLflow registry as "Staging"
         ↓
         Why: Staging first, production second. Allows review before full rollout.
[6] Deployment           → Auto (low risk) or manual approval (high risk)
         ↓
         Why: High-stakes models (medical, financial) need human sign-off.
              Low-stakes models can deploy automatically.
[7] Post-Deploy Watch    → Monitor 24-72h → auto-rollback if degraded

         Why: Production data may differ from evaluation data. Even a model that
              passed step 4 can underperform on real traffic.
```

> **This is identical to a CI/CD pipeline**, with one critical difference: the "tests" in step 4 are statistical comparisons between models, not deterministic pass/fail.

---

## Understanding the Champion vs Challenger Pattern

This pattern is the most important concept in safe model deployment. You'll see it everywhere in production ML.

**Champion:** The model currently serving production traffic. Trusted, proven, known quantity.

**Challenger:** A newly trained model that wants to replace the champion. Untested on production data.

**The rule:** The challenger only gets deployed if it *demonstrably beats* the champion on the same evaluation dataset.

```
 Champion model:   AUC 0.887 on holdout test set
 Challenger model: AUC 0.891 on same holdout test set

 0.891 > 0.887 + 0.005 margin? → No (difference is only 0.004)
 Decision: BLOCK deployment, keep champion

----

 Champion model:   AUC 0.887
 Challenger model: AUC 0.897

 0.897 > 0.887 + 0.005 margin? → Yes
 Decision: DEPLOY challenger, archive champion
```

Why the margin (0.005 in the example above)? Because two models with nearly identical performance aren't meaningfully different. Statistical noise could explain the difference. You only replace the champion if the improvement is clearly real.

**Why this prevents disasters:** Without this gate, a model with a bad random seed (unlucky initialization), trained on a slightly different data slice, could accidentally be deployed and serve worse predictions. The evaluation gate catches this every time.

---

## Prefect CT Pipeline

```python
from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
import mlflow
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

@task
def check_drift_trigger() -> bool:
    reference = load_training_reference()
    production = get_recent_predictions(days=7)
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=production)
    result = report.as_dict()
    psi = result["metrics"][0]["result"]["drift_share"]
    return psi > 0.10

@task
def validate_data(data_path: str) -> bool:
    df = pd.read_parquet(data_path)
    assert df["user_id"].notna().all(),   "Null user_ids found"
    assert (df["amount"] > 0).all(),       "Non-positive amounts found"
    assert df["transaction_id"].nunique() == len(df), "Duplicates found"
    return True

@task
def train_model(data_path: str) -> str:
    df = pd.read_parquet(data_path)
    X_train, X_val, y_train, y_val = prepare_splits(df)
    with mlflow.start_run() as run:
        mlflow.log_params({"data_version": get_dvc_hash(data_path), "git_commit": get_git_hash()})
        model = train(X_train, y_train)
        val_auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
        mlflow.log_metric("val_auc", val_auc)
        mlflow.sklearn.log_model(model, "model", registered_model_name="fraud_detector")
        return run.info.run_id

@task
def evaluate_gate(run_id: str) -> bool:
    challenger = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
    champion   = mlflow.sklearn.load_model("models:/fraud_detector/Production")
    X_test, y_test = load_holdout_test()
    challenger_auc = roc_auc_score(y_test, challenger.predict_proba(X_test)[:, 1])
    champion_auc   = roc_auc_score(y_test, champion.predict_proba(X_test)[:, 1])
    print(f"Champion: {champion_auc:.4f} | Challenger: {challenger_auc:.4f}")
    if challenger_auc < champion_auc - 0.005:
        raise ValueError(f"Challenger worse than champion -- blocking deployment")
    return True

@task
def promote_model(run_id: str):
    client = mlflow.tracking.MlflowClient()
    model_version = get_latest_version("fraud_detector")
    client.transition_model_version_stage(
        name="fraud_detector", version=model_version, stage="Production",
        archive_existing_versions=True
    )
    notify_slack(f"Fraud model v{model_version} promoted to production")

@flow(task_runner=SequentialTaskRunner())
def ct_pipeline():
    should_retrain = check_drift_trigger()
    if not should_retrain:
        print("No drift detected -- skipping retraining")
        return
    validate_data("data/training_latest.parquet")
    run_id = train_model("data/training_latest.parquet")
    gate_passed = evaluate_gate(run_id)
    if gate_passed:
        promote_model(run_id)

if __name__ == "__main__":
    ct_pipeline()
```

---

## Deployment Schedule

```yaml
# Kubernetes CronJob: run CT pipeline weekly
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ct-pipeline
spec:
  schedule: "0 2 * * 1"  # Monday 2am
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: ct-runner
              image: ml-training:latest
              command: ["python", "ct_pipeline.py"]
          restartPolicy: OnFailure
```

---

## Ground Truth Feedback Loop: The Hardest Part

Continuous training requires labels. To know if a model is getting worse, you need the correct answer for past predictions. This sounds obvious but is surprisingly hard in practice.

**The challenge:** You make a prediction now, but you only find out if it was correct later. Sometimes much later.

| Domain | How Labels Arrive | Label Latency | Implication |
|---|---|---|---|
| Fraud detection | Chargeback/dispute filed | 7-30 days | Can retrain at most weekly, using 30-day-old labels |
| Medical diagnosis | Treatment outcome | Months | Quarterly retraining at most |
| Content moderation | User reports | Hours-days | Can retrain daily |
| Click prediction | Click/no-click | Minutes-seconds | Can retrain hourly |

**Why label latency matters:** You cannot retrain faster than labels arrive. If your fraud labels take 30 days to arrive, a weekly retraining schedule uses stale labels — your "new" model is actually trained on old feedback.

**Design implication:** When building a CT system, ask first: "How long until we know if a prediction was correct?" The answer determines your maximum retraining frequency, which determines your entire pipeline architecture.

> **Design the feedback loop from day one.** It's extremely hard to retrofit. The systems that log predictions, link them to outcomes, and build labeled datasets need to be built before you need them.

---

**Design the feedback loop into your system from day one.** Retrain frequency is bounded by label latency.

---

**Next:** [03 -- Safe Deployments →](03-safe-deployments.md)
