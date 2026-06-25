# 05 -- SQL for MLOps Engineers

> SQL is used daily in MLOps -- for feature engineering, data quality checks, training data extraction, and production analysis.

---

## 📚 Prerequisites

This guide assumes you know:
- ✅ SQL basics (SELECT, WHERE, JOIN)
- ✅ GROUP BY and basic aggregations
- ✅ What features are in ML
- ❓ Window functions concept (can learn here)
- ❌ NOT required: Advanced SQL optimization

---

## Why SQL Matters for MLOps

```sql
-- User-level features for fraud detection model
-- This IS what your feature pipeline does
SELECT
    user_id,
    COUNT(*)                                             AS txn_count_30d,
    AVG(amount)                                          AS avg_amount_30d,
    MAX(amount)                                          AS max_amount_30d,
    STDDEV(amount)                                       AS std_amount_30d,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END)       AS fraud_count_30d,
    SUM(CASE WHEN is_foreign = 1 THEN 1 ELSE 0 END)     AS foreign_txn_count_30d,
    AVG(CASE WHEN is_foreign = 1 THEN 1.0 ELSE 0 END)   AS foreign_txn_rate_30d,
    MAX(transaction_time)                                AS last_transaction_time
FROM transactions
WHERE transaction_time >= NOW() - INTERVAL '30 days'
  AND user_id IS NOT NULL
  AND amount > 0
GROUP BY user_id;
```

---

## Window Functions -- Essential for ML

Window functions compute rolling statistics without collapsing rows.

```sql
SELECT
    user_id,
    transaction_time,
    amount,

    -- Rolling 7-transaction average for this user (time-ordered)
    AVG(amount) OVER (
        PARTITION BY user_id
        ORDER BY transaction_time
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS avg_last_7_txns,

    -- Time since previous transaction (in hours)
    EXTRACT(EPOCH FROM (
        transaction_time - LAG(transaction_time) OVER (
            PARTITION BY user_id ORDER BY transaction_time
        )
    )) / 3600 AS hours_since_last_txn,

    -- Running total for user this month
    SUM(amount) OVER (
        PARTITION BY user_id, DATE_TRUNC('month', transaction_time)
        ORDER BY transaction_time
    ) AS running_monthly_total,

    -- Rank by amount for this user (largest = rank 1)
    RANK() OVER (
        PARTITION BY user_id
        ORDER BY amount DESC
    ) AS amount_rank

FROM transactions
WHERE transaction_time >= '2024-01-01';
```

---

## Data Quality Queries (Run Before Every Training Job)

```sql
-- 1. Null rates per column
SELECT
    COUNT(*)                                                        AS total_rows,
    SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS user_id_null_pct,
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*)  AS amount_null_pct,
    SUM(CASE WHEN is_fraud IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS label_null_pct
FROM transactions
WHERE transaction_time >= NOW() - INTERVAL '7 days';

-- 2. Class balance
SELECT
    is_fraud,
    COUNT(*)                                              AS count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()             AS percentage
FROM transactions
GROUP BY is_fraud;

-- 3. Duplicate detection
SELECT transaction_id, COUNT(*) AS occurrences
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1
LIMIT 20;  -- any rows here = problem

-- 4. Distribution statistics for drift monitoring
SELECT
    PERCENTILE_CONT(0.01) WITHIN GROUP (ORDER BY amount) AS p01,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY amount) AS p50,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) AS p75,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY amount) AS p99,
    AVG(amount)                                            AS mean,
    STDDEV(amount)                                         AS std_dev
FROM transactions
WHERE transaction_time >= NOW() - INTERVAL '7 days';
```

---

## CTEs -- Readable Multi-Step Queries

```sql
-- Build training dataset step by step (readable, maintainable)
WITH
-- Step 1: Recent transactions
recent_transactions AS (
    SELECT *
    FROM transactions
    WHERE transaction_time BETWEEN '2024-01-01' AND '2024-06-30'
      AND amount > 0
),

-- Step 2: User-level features
user_features AS (
    SELECT
        user_id,
        COUNT(*)         AS txn_count,
        AVG(amount)      AS avg_amount,
        SUM(is_fraud)    AS fraud_count
    FROM recent_transactions
    GROUP BY user_id
),

-- Step 3: Join with user profile
enriched AS (
    SELECT
        uf.*,
        up.credit_score,
        up.account_age_days,
        up.country
    FROM user_features uf
    LEFT JOIN user_profiles up ON uf.user_id = up.user_id
)

-- Final: select features for training
SELECT * FROM enriched
WHERE txn_count >= 5    -- only users with enough history
  AND credit_score IS NOT NULL;
```

---

## JOINs for ML Data Preparation

```sql
-- LEFT JOIN: keep all transactions even if user profile missing
SELECT
    t.transaction_id,
    t.user_id,
    t.amount,
    t.is_fraud,                  -- ← label

    -- User profile features (NULL if profile missing → impute later)
    u.credit_score,
    u.account_age_days,
    u.country,

    -- Merchant features
    m.merchant_fraud_rate_90d,
    m.merchant_category

FROM transactions t
LEFT JOIN user_profiles u   ON t.user_id = u.user_id
LEFT JOIN merchant_stats m  ON t.merchant_id = m.merchant_id
WHERE t.transaction_time >= '2024-01-01'
  AND t.transaction_time <  '2024-07-01';
```

---

## Production Monitoring Queries

```sql
-- Model prediction distribution: is the model behaving normally?
SELECT
    DATE_TRUNC('hour', predicted_at)      AS hour,
    COUNT(*)                               AS total_predictions,
    AVG(fraud_probability)                 AS avg_fraud_prob,
    SUM(CASE WHEN fraud_probability > 0.5 THEN 1 ELSE 0 END) AS flagged_count,
    SUM(CASE WHEN fraud_probability > 0.5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS flag_rate
FROM model_predictions
WHERE predicted_at >= NOW() - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', predicted_at)
ORDER BY hour;
-- Alert if flag_rate changes significantly from historical average
```

---

**Next:** [06 -- Async Python →](06-async-python.md)
