# 02 -- Portfolio Strategy & Career Growth

## Prerequisites

**For this to work:** You've already completed at least 5 MLOps projects (doesn't matter if small). You have a GitHub account. You've written some technical writing or documentation before.

**Mindset:** This is a 24-month strategy, not a quick path. Consistency over sprints. Building in public requires some vulnerability -- get comfortable with that.

> The engineers who reach top 0.1% build in public, contribute to open source, and let their work speak for them.

## Why This Matters (The Recruiter's Perspective)

Recruiters screen 100+ resumes per role. Top companies (Netflix, Stripe, Airbnb, Lambda Labs) skip the resume entirely for proven MLOps engineers. They look for: public GitHub repos, blog posts showing deep technical thinking, open source contributions. These signal: you know what you're doing, you can communicate about it, you've validated your knowledge in production.

---

## The GitHub Portfolio Structure

Every project should follow this structure:

```
fraud-detection-mlops/
├── README.md               ← CRITICAL: first thing everyone reads
│   ├── What problem this solves (1 sentence)
│   ├── Architecture diagram (draw.io or mermaid)
│   ├── Tech stack with versions
│   ├── Measured results (latency, throughput, cost)
│   └── How to run it
├── src/
│   ├── features/           ← feature engineering code
│   ├── training/           ← training pipeline
│   └── serving/            ← serving code + Dockerfile
├── infrastructure/
│   ├── k8s/                ← Kubernetes manifests
│   └── terraform/          ← infrastructure as code
├── tests/                  ← all test levels (data, model, pipeline, gate)
└── docs/
    └── architecture.md     ← Architecture Decision Records
```

---

## Technical Blog Strategy

One blog post per completed project. Target: 1 post/month.

**What makes a blog post get read and shared:**

```
NOT: "Here's how MLflow works" (already covered everywhere)

YES: "Why our MLflow tracking server was losing runs under high load --
      and how we fixed it with connection pooling"

YES: "The subtle feature store bug that caused training-serving skew
      for 3 months before we caught it"

YES: "How I built a production MLOps stack for under $50/month on a VPS"
      (your unique Nepal/VPS angle -- nobody else has this story)
```

**Blog post structure that works:**

```
Title: Specific problem + what you did about it
       "How I reduced model serving costs 80% with ONNX quantization"

Hook (100 words): The problem and why it matters

The Story (300 words):
  - What you tried first and why it didn't work
  - The insight that unlocked the solution

The Solution (400 words):
  - Architecture or approach
  - Key code snippet (production quality)

The Results (100 words):
  - Before/after numbers (latency, cost, throughput)
  - What you'd do differently

Conclusion (50 words): Next steps, what you learned
```

---

## LinkedIn Post Template for Projects

```
Just shipped: [Project Name] 🚀

Problem I solved:
[One sentence describing the business/engineering problem]

What I built:
• [Technical component 1]
• [Technical component 2]
• [Technical component 3]

Stack: [Tool 1] + [Tool 2] + [Tool 3] + [Tool 4]

Results:
• [Metric 1]: before → after (X% improvement)
• [Metric 2]: before → after

Full writeup: [blog link]
Code: [github link]

#MLOps #MachineLearning #DevOps #Python
```

---

## Open Source Contribution Path

Start small. Don't start with features.

```
Month 1: Documentation fixes
  → Use the tool seriously
  → When something confuses you, the docs are wrong/missing
  → Fix them. PR merged in < 48h usually.

Month 2: Bug reproductions
  → Find an open issue with vague reproduction steps
  → Reproduce it, add minimal reproduction script
  → Comment in the issue: "I reproduced this with: ..."
  → Maintainers love this -- no code change needed

Month 3: Fix a "good first issue"
  → Every serious OSS project labels these
  → Small, scoped, maintainer willing to guide you

Month 4+: Small bug fixes, then features
  → Comment BEFORE implementing: "I'd like to fix this by X approach"
  → Get maintainer buy-in before writing code

Target projects for MLOps: Feast, Evidently AI, Prefect, MLflow, ZenML
```

---

## The Outreach Message That Gets Responses

```
Subject: ML Platform Engineer -- [something specific about them]

Hi [Name],

I noticed [company] is [specific thing you observed -- recent job post,
blog post, open source project they use] related to ML infrastructure.

I'm an MLOps/ML Platform engineer specializing in Kubernetes-native ML
systems -- specifically the gap between "model works in notebook" and
"model is reliable in production."

What I've shipped recently:
• Feature store (Feast + Redis) serving sub-20ms predictions [GitHub]
• Automated CT pipeline with drift-based triggers, reducing manual
  retraining from weekly manual effort to fully automated [Blog post]
• Shadow → canary deployment framework that cut production incidents 60% [GitHub]

I'm based in Nepal, available for remote work, timezone UTC+5:45
(good overlap with EU and partial overlap with US East).

Would a 20-minute call make sense?

Suchan
suchanmadhikarmi.com.np | github.com/SuchanMadhikarmi
```

---

## The 24-Month Blueprint

**Months 1-6:** Build Projects P-01 to P-06 publicly on GitHub
  → 6 public repos with clean READMEs
  → 6 blog posts (one per project)
  → Start appearing in MLOps Slack communities

**Months 7-12:** Advanced projects + first open source contribution
  → Projects P-07, P-08
  → Merged PR in Feast or Evidently
  → Write your defining post: "How I built production MLOps for $50/month"

**Months 13-18:** Projects P-09, P-10 + niche authority
  → Kubernetes-native MLOps is your specialty
  → Active in community (answering questions, GitHub issues)
  → Recruiters start appearing in your LinkedIn

**Months 19-24:** First USD remote opportunity
  → 9 public projects + 15+ blog posts + 2-3 OSS contributions
  → Direct outreach to 20 ML-heavy Series B/C startups
  → First contract or role landed → the flywheel starts

---
