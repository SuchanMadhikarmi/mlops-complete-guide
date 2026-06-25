# MLOps Complete Guide

Production-grade machine learning systems reference for engineers who operate infrastructure at scale.

This repository documents the operational patterns, architectural decisions, and engineering practices required to build and maintain ML systems that work reliably in production. Written from an infrastructure engineering perspective, tested in real deployments, focused on what actually breaks and how to prevent it.

---

## Purpose and Scope

Most MLOps documentation teaches tool syntax. This guide addresses the harder questions: why these tools exist, what production failure modes they prevent, how architectural decisions compound over time, and what the maintenance burden looks like six months after deployment.

The target audience is engineers with production systems experience who need to understand ML-specific operational concerns. If you have built distributed systems, operated databases, or managed infrastructure, this content assumes that background and builds on it.

### What This Covers

- ML system lifecycle from experimentation through production operation
- Infrastructure patterns specific to ML workloads (GPUs, distributed training, model serving)
- Operational concerns that differ from traditional software (data drift, training-serving skew, silent degradation)
- Production-tested implementations with failure modes documented
- Cost optimization strategies for compute-intensive workloads
- Team organization and workflow patterns that scale

### What This Excludes

- Programming language tutorials
- ML algorithm theory or mathematical foundations
- Cloud platform marketing comparisons
- Tool advocacy or vendor positioning
- Toy datasets or contrived examples

---

## Repository Structure

The content is organized in learning order, with each section building on previous concepts:

### Foundation Layer

**ml-fundamentals/** - Engineering perspective on how ML systems work. Covers training mechanics, model types, evaluation metrics, and data handling. Required reading before operational topics.

**supporting-knowledge/** - Adjacent domains that inform MLOps decisions. Statistics for monitoring, data engineering patterns, cloud architecture, security considerations, design patterns, and Python ecosystem specifics.

### Operational Layer

**core-mlops/** - Essential production capabilities. Experiment tracking (MLflow), data versioning (DVC), model serving (FastAPI patterns), CI/CD for ML workflows, and monitoring infrastructure (Prometheus/Grafana).

**production-engineering/** - Advanced reliability patterns. Feature stores, continuous training pipelines, deployment strategies (shadow/canary), drift detection mechanisms, model explainability, and inference architecture (batch/streaming/real-time).

**practical-skills/** - Hands-on implementation knowledge. Docker for ML containers, Kubernetes for ML workloads, testing strategies, systematic debugging, SQL for feature engineering, asynchronous Python patterns.

### Advanced Topics

**advanced-specialized/** - Expert-level systems. Distributed training (Ray, DeepSpeed), Kubernetes-native orchestration (KFP, Argo), model compression and optimization, multi-model serving (Triton), ML platform architecture.

**llmops/** - Large language model operations. RAG architectures, fine-tuning patterns, prompt management, safety guardrails, high-throughput serving (vLLM).

### Career Development

**career/** - Interview preparation and portfolio strategy. System design frameworks, behavioral interview patterns, portfolio project structure, open source contribution path.

**projects/** - Ten progressive portfolio projects with full specifications, from basic MLflow setup to complete self-hosted ML platform.

---

## Learning Progression

The material follows a deliberate progression. Each phase builds skills required for the next:

### Phase 0: Foundation (4-6 weeks)

Establish mental models for how ML systems differ from traditional software. Understand training mechanics, evaluation strategies, and data handling patterns. Without this foundation, operational decisions lack context.

Start: `ml-fundamentals/00-why-mlops-is-different.md`  
Complete: All files in `ml-fundamentals/`  
Outcome: Can read ML code and understand operational implications

### Phase 1: Core Infrastructure (8-10 weeks)

Build the essential operational capabilities every production ML team requires. Implement experiment tracking, data versioning, model serving, CI/CD, and monitoring. These are table stakes.

Complete: `core-mlops/` + Projects P-01 through P-03  
Outcome: Can build reproducible ML pipelines with basic observability

### Phase 2: Production Hardening (10-12 weeks)

Implement reliability patterns that prevent common production failures. Feature stores eliminate training-serving skew, continuous training pipelines automate model updates, deployment strategies enable safe rollouts.

Complete: `production-engineering/` + Projects P-04 through P-06  
Outcome: Can operate ML systems with production-grade reliability

### Phase 3: Advanced Systems (12-16 weeks)

Optimize for scale and efficiency. Distributed training for large models, Kubernetes-native orchestration for isolation, model compression for cost reduction, multi-model serving for operational efficiency.

Complete: `advanced-specialized/` + Projects P-07 through P-09  
Outcome: Can architect and operate enterprise ML platforms

### Phase 4: Sustained Excellence (ongoing)

Document decisions, contribute improvements upstream, build tools others rely on. The distinguishing characteristic of senior infrastructure engineers.

---

## Key Insights from Production Experience

These are the lessons learned from operating ML systems at scale:

**Data versioning is more critical than model versioning.** Model artifacts without data provenance cannot be reproduced. Every training run must log the exact data hash, not just the data location. The S3 path "latest" means nothing six months later.

**Three types of drift require different responses.** Data drift (input distribution changed) signals retraining with updated data. Concept drift (relationship changed) requires feature re-engineering. Label drift (target distribution changed) needs threshold retuning. Teams waste weeks retraining when the problem is concept drift.

**The production model is 10x the notebook.** A working prototype demonstrates feasibility. The production system handles null inputs, schema evolution, model versioning, latency requirements, memory constraints, monitoring, retraining triggers, audit logging, and graceful degradation. This is where the engineering work lives.

**Shadow mode before A/B testing.** Running a new model on production traffic with predictions logged but not served provides real-world validation with zero user impact. Any business-critical model should run in shadow for 48-72 hours before serving predictions.

**Experiment tracking needs discipline.** Logging runs without capturing git commit, data version, environment specifications, all hyperparameters, and random seeds produces irreproducible results. Reproduction is not retroactive.

**model.eval() is not optional.** PyTorch models without model.eval() before inference keep dropout active. Predictions become non-deterministic. There is no error message. This is a silent production bug that can take days to diagnose.

**Feature stores solve training-serving skew.** Computing the same feature differently in training and serving means the model receives inputs during serving that do not match its training distribution. Predictions degrade silently. Feature stores enforce a single definition used in both contexts.

---

## For Infrastructure Engineers

If you operate production systems, you already have most of the skills required for MLOps. The infrastructure fundamentals are the same: containers, orchestration, CI/CD, observability, incident response, capacity planning.

The new concepts are domain-specific: statistical process control for monitoring (PSI, KL divergence), ML-specific failure modes (concept drift, training-serving skew), and the tooling layer (MLflow, Feast, Evidently, KFP). None of these are conceptually more difficult than distributed systems or database internals. They are simply unfamiliar.

The advantage you bring is an operational mindset. You think about failure modes, maintenance burden, on-call load, and systems that need to work at 3am without manual intervention. These are exactly the perspectives missing from most ML engineering.

---

## Interview Preparation

MLOps interviews evaluate production systems experience through pattern recognition. The ability to describe a system you built, including failure modes encountered and architectural changes made in response, carries more weight than theoretical knowledge.

System design interviews follow a predictable structure:

1. Clarify the problem: What exactly is the model predicting?
2. Establish requirements: What latency is required? At what scale?
3. Design data flow: How does ground truth flow back to training?
4. Address failure modes: What breaks and how do you detect it?

These four questions determine every meaningful architectural decision. Everything else is implementation detail.

See `career/01-interview-guide.md` for comprehensive preparation including specific questions, framework-based answers, and behavioral interview patterns.

---

## Portfolio Projects

Theory without implementation is academic. These ten projects provide concrete evidence of capability:

**P-01:** MLflow tracking server (PostgreSQL + MinIO) - Production experiment tracking  
**P-02:** DVC data pipeline with validation - Reproducible data versioning  
**P-03:** FastAPI serving with monitoring - Production-grade model API  
**P-04:** GitHub Actions ML CI/CD - Automated deployment with gates  
**P-05:** Grafana ML observability - Model-level monitoring  
**P-06:** Continuous training pipeline - Autonomous retraining  
**P-07:** Shadow + canary framework - Safe deployment patterns  
**P-08:** Feast feature store - Training-serving consistency  
**P-09:** Kubernetes-native ML pipeline - Enterprise orchestration  
**P-10:** End-to-end ML platform - Complete self-hosted system  

Full specifications with architecture requirements, evaluation criteria, and failure mode documentation in `projects/10-portfolio-projects.md`.

---

## Quick Start Paths

### For DevOps/SRE Engineers New to ML

1. Read `ml-fundamentals/00-why-mlops-is-different.md` (15 min)
2. Read `supporting-knowledge/00-devops-to-mlops-translation.md` (15 min)
3. Skim `GLOSSARY.md` for vocabulary reference (10 min)
4. Continue with `ml-fundamentals/` in order

### For Software Engineers Learning MLOps

1. Start with `ml-fundamentals/` for foundation
2. Move to `core-mlops/` for essential infrastructure
3. Build Projects P-01, P-02, P-03 to solidify concepts

### For Experienced ML Engineers Learning Production Operations

1. Skip to `production-engineering/` if fundamentals are solid
2. Focus on `advanced-specialized/` for scaling patterns
3. Build Projects P-04 through P-09

### For Interview Preparation

1. Review `career/01-interview-guide.md` for framework
2. Study `production-engineering/` for system design depth
3. Practice explaining Projects P-06, P-07, P-08 (most impressive)

---

## Contributing

Valuable contributions come from production experience: corrections based on real deployments, additional failure modes encountered, architectural patterns that solved specific problems, cost optimization strategies that worked.

Not needed: tool tutorials duplicating official documentation, beginner-level rewrites, vendor comparisons, theoretical additions without operational grounding.

Process: Open an issue describing the production context and proposed change. PRs with real-world grounding are prioritized. See `CONTRIBUTING.md`.

---

## Technical Accuracy

This content reflects production experience across multiple deployments. Architectural patterns and operational guidance are field-tested. Cost estimates are based on actual cloud bills. Failure modes are documented from real incidents.

That said, technology evolves. If you find outdated information, incorrect technical details, or better approaches that emerged since writing, corrections are welcome.

---

## Author

Suchan Madhikarmi  
DevOps → MLOps transition  
Kathmandu, Nepal

Built this guide to document structured learning for infrastructure engineers moving into ML operations. Particular focus on engineers from DevOps/SRE backgrounds who find most ML content assumes data science foundations.

Website: [suchanmadhikarmi.com.np](https://suchanmadhikarmi.com.np)  
LinkedIn: [linkedin.com/in/suchanmadhikarmi](https://linkedin.com/in/suchanmadhikarmi)  
GitHub: [github.com/SuchanMadhikarmi](https://github.com/SuchanMadhikarmi)

---

## License

MIT License - Use freely, modify as needed, attribution appreciated but not required.

For questions, corrections, or discussion: open an issue or reach out directly.
