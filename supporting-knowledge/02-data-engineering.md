# 02 — Data Engineering for MLOps

## Prerequisites

**SQL knowledge:** Comfortable writing SELECT, WHERE, GROUP BY, JOIN queries. Can read a schema and understand table relationships.

**DevOps/Infrastructure perspective:** Understand what "data pipeline" means. Familiar with scheduling concepts (cron jobs, DAGs).

**ML context:** Know why data quality matters for model training. Have trained a model on real data.

**Required tools:** Python · Pandas · SQL · Basic familiarity with cloud storage (S3/GCS)

> The data pipeline before your model is where 80% of production problems originate. Understanding data engineering makes you a dramatically more effective MLOps engineer.

## Why This Matters (The DevOps Translation)

Data engineering for ML is like infrastructure for software:

- Bad data = bad models, even with perfect ML code
- Data pipeline uptime matters just as much as application uptime
- "Why did the model fail?" → usually a data pipeline problem, not a model problem

Understanding this perspective changes how you build ML systems.

---

## Batch vs Streaming Ingestion

### Batch Ingestion
Collect data in large chunks on a schedule. Simple, cheap, data is hours old.

```python
# Airflow DAG: nightly batch ingestion
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def ingest_daily_transactions():
    query = """
        SELECT * FROM transactions
        WHERE DATE(created_at) = CURRENT_DATE - 1
    """
    df = pd.read_sql(query, db_connection)
    df.to_parquet(f"s3://data-lake/bronze/transactions/{date.today()}.parquet")

dag = DAG("daily_transaction_ingestion", schedule_interval="@daily")
task = PythonOperator(task_id="ingest", python_callable=ingest_daily_transactions, dag=dag)
```

### Streaming Ingestion (Kafka)
Data flows continuously, processed in seconds. Required for real-time fraud detection.

```python
from confluent_kafka import Producer, Consumer
import json

# Producer: send events to Kafka
producer = Producer({"bootstrap.servers": "kafka:9092"})

def send_transaction(transaction: dict):
    producer.produce(
        topic="transactions",
        key=transaction["user_id"].encode(),
        value=json.dumps(transaction).encode()
    )
    producer.flush()

# Consumer: receive and process events
consumer = Consumer({
    "bootstrap.servers": "kafka:9092",
    "group.id": "fraud-detection-service",
    "auto.offset.reset": "latest"
})
consumer.subscribe(["transactions"])

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        continue
    transaction = json.loads(msg.value().decode())
    fraud_score = model.predict(transaction)
    # Handle result...
```

---

## Medallion Architecture

The standard pattern for organizing data in a modern data lakehouse.

```
Bronze (Raw)  →  Silver (Clean)  →  Gold (Features)
Store raw         Deduplicated       ML-ready
as-is             Validated          Aggregated
Never delete      Typed              Feature store ready
```

```python
# Bronze → Silver transformation
def bronze_to_silver(bronze_path: str, silver_path: str):
    df = pd.read_parquet(bronze_path)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=["transaction_id"])
    
    # Type enforcement
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    
    # Remove invalid records
    df = df[df["amount"] > 0]
    df = df[df["user_id"].notna()]
    
    df.to_parquet(silver_path, index=False)

# Silver → Gold (feature engineering)
def silver_to_gold(silver_path: str, gold_path: str):
    df = pd.read_parquet(silver_path)
    
    # User-level aggregations (ML features)
    user_features = df.groupby("user_id").agg(
        avg_amount_30d=("amount", "mean"),
        txn_count_30d=("transaction_id", "count"),
        max_amount_30d=("amount", "max"),
        fraud_count_90d=("is_fraud", "sum")
    ).reset_index()
    
    user_features.to_parquet(gold_path, index=False)
```

**Why Bronze-Silver-Gold?** Failure at any step only affects downstream. If Silver transformation has a bug, you fix it and re-run from Bronze. Original data always preserved.

---

## Delta Lake — Time Travel for ML

Delta Lake adds ACID transactions and time travel to your data lake (S3/GCS).

```python
from delta import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .getOrCreate()

# Write as Delta table
df.write.format("delta").save("s3://data-lake/gold/user_features")

# Time travel — read data as it was on a specific date
# Critical for point-in-time correct training data
historical_features = spark.read \
    .format("delta") \
    .option("timestampAsOf", "2024-01-15T00:00:00") \
    .load("s3://data-lake/gold/user_features")

# Or by version number
version_5_features = spark.read \
    .format("delta") \
    .option("versionAsOf", 5) \
    .load("s3://data-lake/gold/user_features")
```

**Why this matters for reproducibility:** Can train on exact data from 6 months ago. Reproducing old model from old data becomes trivial.

---

## Apache Spark — Processing Large Data

When your dataset exceeds RAM, use Spark to distribute processing across a cluster.

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("FeatureEngineering") \
    .config("spark.executor.memory", "8g") \
    .config("spark.executor.cores", "4") \
    .getOrCreate()

# Read 100TB of transactions (distributed across cluster)
transactions = spark.read.parquet("s3://data-lake/silver/transactions/")

# Feature engineering at scale
user_features = transactions \
    .filter(F.col("status") == "completed") \
    .groupBy("user_id") \
    .agg(
        F.avg("amount").alias("avg_transaction_30d"),
        F.count("*").alias("transaction_count_30d"),
        F.sum(F.when(F.col("is_fraud") == 1, 1).otherwise(0)).alias("fraud_count"),
        F.max("amount").alias("max_transaction_30d")
    )

# Write features to Gold layer
user_features.write \
    .format("delta") \
    .mode("overwrite") \
    .save("s3://data-lake/gold/user_features")

# This runs across 100 machines in parallel
# 100TB → processed in minutes instead of hours
```

---

## dbt — Data Transformations as Code

dbt turns SQL transformations into version-controlled, tested, documented pipelines.

```sql
-- models/gold/user_features.sql
-- This runs in your data warehouse (BigQuery, Snowflake, Redshift)

{{ config(materialized='table') }}

WITH recent_transactions AS (
    SELECT *
    FROM {{ ref('silver_transactions') }}  -- dbt handles dependencies
    WHERE transaction_time >= CURRENT_DATE - 30
),

user_stats AS (
    SELECT
        user_id,
        COUNT(*)                                          AS txn_count_30d,
        AVG(amount)                                       AS avg_amount_30d,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END)   AS fraud_count_30d
    FROM recent_transactions
    GROUP BY user_id
)

SELECT * FROM user_stats
```

```yaml
# schema.yml — tests defined as code
models:
  - name: user_features
    columns:
      - name: user_id
        tests:
          - not_null
          - unique
      - name: avg_amount_30d
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
```

```bash
dbt run        # execute transformations
dbt test       # run all data tests
dbt docs serve # generate and serve documentation
```

---

## Data Quality Checklist for ML

```python
def ml_data_quality_check(df: pd.DataFrame, config: dict) -> bool:
    """Run before every training job. Returns False if data is bad."""
    
    checks_passed = True
    
    # 1. Minimum rows
    if len(df) < config.get("min_rows", 1000):
        print(f"FAIL: Only {len(df)} rows (min: {config['min_rows']})")
        checks_passed = False
    
    # 2. Null rates
    for col, max_null_pct in config.get("max_null_rates", {}).items():
        actual = df[col].isnull().mean()
        if actual > max_null_pct:
            print(f"FAIL: {col} null rate {actual:.1%} > {max_null_pct:.1%}")
            checks_passed = False
    
    # 3. Value ranges
    for col, (min_val, max_val) in config.get("value_ranges", {}).items():
        out_of_range = ~df[col].between(min_val, max_val)
        if out_of_range.any():
            print(f"FAIL: {col} has {out_of_range.sum()} out-of-range values")
            checks_passed = False
    
    # 4. No duplicates
    dup_col = config.get("unique_column")
    if dup_col and df[dup_col].duplicated().any():
        print(f"FAIL: Duplicate values in {dup_col}")
        checks_passed = False
    
    # 5. Class balance
    target = config.get("target_column")
    if target:
        pos_rate = df[target].mean()
        min_rate, max_rate = config.get("target_range", (0.0001, 0.5))
        if not (min_rate <= pos_rate <= max_rate):
            print(f"FAIL: Target rate {pos_rate:.4%} outside [{min_rate:.4%}, {max_rate:.4%}]")
            checks_passed = False
    
    if checks_passed:
        print(f"✓ All data quality checks passed ({len(df):,} rows)")
    
    return checks_passed
```

---

**Next:** [03 — Cloud Platforms →](03-cloud-platforms.md)
