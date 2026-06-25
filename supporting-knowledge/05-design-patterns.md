# 05 — ML Design Patterns


## Prerequisites

**ML systems experience:** Have built at least 2-3 production ML systems. Know what recommendation systems, classification, and ranking look like.

**Architecture thinking:** Understand microservices, data flow, system bottlenecks.

**Required understanding:** Design patterns are recurring solutions to common problems. You need experience with the "common problems" first.

> Recurring solutions to common ML architecture problems. Like software design patterns, but for ML systems.
> Recurring solutions to common ML architecture problems. Like software design patterns, but for ML systems.

---

## Pattern 1 — Two-Tower Model (Recommendation at Scale)

**Problem:** 10M users × 10M products = 100 trillion pairs. Can't score all combinations at serving time.

**Solution:** Two separate neural networks that share a training objective but run independently.

```
Tower 1 (User Tower)          Tower 2 (Item Tower)
Input: user features      +   Input: item features
Output: user embedding        Output: item embedding
(128 numbers)                 (128 numbers)

Trained so that:
  user_embedding · item_embedding → high if user likes item
```

**Serving flow:**
```
Step 1 (offline, once): Run ALL 10M items through Item Tower
                         Store item_embeddings in Qdrant

Step 2 (online, per request): Run THIS user through User Tower
                               Get user_embedding (128 numbers)

Step 3: Vector search in Qdrant
         Find 100 items with most similar embeddings to user
         Return as recommendations
         Latency: ~5ms regardless of catalog size
```

This is how YouTube, Spotify, Netflix, and every major recommendation system works at scale.

---

## Pattern 2 — Champion/Challenger

**Problem:** How do you safely test whether a new model is better?

**Solution:** Run both simultaneously, route a small percentage to challenger, compare metrics.

```python
class ChampionChallengerRouter:
    def __init__(self, champion, challenger, challenger_pct=10):
        self.champion = champion
        self.challenger = challenger
        self.challenger_pct = challenger_pct
        self.metrics = {"champion": [], "challenger": []}
    
    def route_and_predict(self, request_id: str, features):
        import hashlib
        bucket = int(hashlib.md5(request_id.encode()).hexdigest(), 16) % 100
        
        if bucket < self.challenger_pct:
            pred = self.challenger.predict(features)
            model_used = "challenger"
        else:
            pred = self.champion.predict(features)
            model_used = "champion"
        
        return pred, model_used
```

**Variants:**
- Multi-challenger: test 3+ models simultaneously
- Bandit routing: dynamically increase traffic to winning model
- Epsilon-greedy: 90% champion, 10% exploration

---

## Pattern 3 — Multi-Armed Bandit

**Problem:** A/B testing wastes traffic on bad variants. How do you learn AND optimize simultaneously?

**Analogy:** 10 slot machines. Unknown payout rates. How do you maximize winnings while figuring out which is best?

```python
import numpy as np

class ThompsonSamplingBandit:
    """
    Thompson Sampling: maintains probability distribution over each model's
    true quality. Samples from distributions to pick which model to use.
    As evidence accumulates, the best model gets more traffic automatically.
    """
    
    def __init__(self, model_names: list):
        self.models = model_names
        # Beta distribution parameters: alpha=successes+1, beta=failures+1
        self.alpha = {m: 1.0 for m in model_names}  # successes
        self.beta = {m: 1.0 for m in model_names}   # failures
    
    def select_model(self) -> str:
        """Sample from each model's distribution, pick highest."""
        samples = {
            model: np.random.beta(self.alpha[model], self.beta[model])
            for model in self.models
        }
        return max(samples, key=samples.get)
    
    def update(self, model: str, success: bool):
        """Update after observing outcome."""
        if success:
            self.alpha[model] += 1
        else:
            self.beta[model] += 1

# Usage
bandit = ThompsonSamplingBandit(["model_v22", "model_v23", "model_v24"])

for request in production_traffic:
    model = bandit.select_model()
    prediction = models[model].predict(request.features)
    
    # Later, when outcome is known:
    outcome = get_outcome(request.id)  # was prediction correct?
    bandit.update(model, success=outcome)
    
# After 10,000 requests, traffic will have concentrated on the best model
```

---

## Pattern 4 — Embedding Store

**Problem:** Everything is an embedding now (text, users, products, images). Need a unified way to store and search them.

```python
# Everything becomes a vector → stored in vector database → searchable by similarity

# Text embeddings
text_embedding = embed("How do I reset my password?")  # [0.2, -0.4, 0.8, ...]

# User embeddings (from Two-Tower)
user_embedding = user_tower.predict(user_features)     # [0.1, 0.3, -0.2, ...]

# Product embeddings
product_embedding = embed(product_description)          # [0.5, -0.1, 0.7, ...]

# All stored in Qdrant, all searchable:
similar_questions = qdrant.search("faq_collection", text_embedding, top_k=5)
recommended_products = qdrant.search("products", user_embedding, top_k=20)
```

**Key insight:** Once everything is an embedding, you can measure similarity between ANY two things using the same infrastructure.

---

## Pattern 5 — Feedback Loop Monitoring

**Problem:** Your model influences what data you collect, which affects your next model. Without monitoring, biases compound.

```python
def monitor_feedback_loop(current_model_data, original_data):
    """
    Detect when model decisions are contaminating training data.
    
    Example: Credit scoring model denies loans to group X.
             Group X now has less data in system.
             Next model trained on even less data from X.
             Next model denies X even more.
    """
    
    # Check representation drift in training data
    for demographic in ["age_group", "gender", "country"]:
        current_dist = current_model_data[demographic].value_counts(normalize=True)
        original_dist = original_data[demographic].value_counts(normalize=True)
        
        for group in original_dist.index:
            if group in current_dist:
                change = (current_dist[group] - original_dist[group]) / original_dist[group]
                if abs(change) > 0.20:  # > 20% change in representation
                    alert(f"Representation drift: {demographic}={group} changed {change:+.1%}")
    
    # Check if denial rates by group are trending
    denial_rates = current_model_data.groupby("demographic")["was_denied"].mean()
    for group, rate in denial_rates.items():
        if rate > 0.7:  # >70% denial for any group
            alert(f"High denial rate for {group}: {rate:.1%} — check for feedback loop")
```

---

## Pattern 6 — Medallion Architecture (Data Layer)

Already covered in Data Engineering, but summarized here as a design pattern:

```
Bronze Layer: Raw data exactly as received. Never modify, never delete.
              → Source of truth for data lineage

Silver Layer: Cleaned, validated, typed, deduplicated.
              → Reprocess from Bronze if logic changes

Gold Layer:   Business aggregations, ML features.
              → Input to Feature Store and model training

Rule: Data flows downstream only. No writing back to upstream layers.
Rule: A bug in Silver? Fix the transformation, re-run from Bronze.
Rule: Training data always comes from Gold, never Bronze/Silver directly.
```

---

**Next:** [06 — Python Ecosystem →](06-python-ecosystem.md)
