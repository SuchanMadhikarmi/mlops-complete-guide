# Glossary

Precise definitions of every term used in this guide and in production MLOps work generally. Written for engineers who want to understand what a term actually means, not just be able to use it in a sentence.

---

## A

**A/B Testing (Model)**
Running two model versions simultaneously on live traffic, with users assigned to groups through consistent hashing. Unlike shadow mode, both groups receive real predictions from their respective models. The point is to measure business outcomes — conversion rate, click-through rate, revenue — rather than offline metrics. Requires pre-calculated sample sizes, consistent user assignment, and defined stopping criteria before the experiment begins. Running an A/B test without these produces results you cannot trust.

**Accuracy**
The fraction of total predictions that were correct. Widely reported, rarely the right metric. On a dataset where 99% of samples are class zero, a model that predicts class zero for everything achieves 99% accuracy while being completely useless. Use precision, recall, F1, or AUC for classification problems where classes are not perfectly balanced.

**Adversarial Example**
An input that has been modified in a small, often imperceptible way specifically to cause a model to produce an incorrect output. The modification exploits the geometry of the model's decision boundary. Relevant to any system where inputs could be controlled by an adversary — fraud detection, content moderation, biometric authentication.

**Artifact**
Any file produced during the ML lifecycle that needs to be stored, versioned, and referenced. Model weights, preprocessors, evaluation reports, confusion matrices, and feature schemas are all artifacts. An experiment tracking system that only logs metrics without artifacts is capturing incomplete information.

**AutoML**
Automated machine learning — systems that automate the selection of model architecture, feature engineering, and hyperparameter tuning. Useful as a baseline and for prototyping. Not a replacement for understanding what it is doing.

---

## B

**Backpropagation**
The algorithm used to compute gradients in a neural network. Works by applying the chain rule of calculus backward through the computational graph, from the loss to the input. The gradients it produces tell the optimizer how much and in which direction to adjust each weight. Understanding this is necessary for diagnosing training failures involving vanishing or exploding gradients.

**Batch Inference**
Running model predictions on a large dataset at once, on a schedule, with results stored for later retrieval. The opposite of real-time inference. Appropriate when predictions do not need to be fresh at the moment of consumption — nightly credit score updates, weekly churn predictions, daily recommendation refreshes. Cheaper and simpler to operate than real-time serving.

**Batch Normalization**
A technique that normalizes layer activations across the batch dimension during training. Stabilizes training and allows higher learning rates. Has a critical production implication: it behaves differently in training mode and inference mode. In training mode it uses batch statistics; in inference mode it uses running statistics accumulated during training. Failing to switch to inference mode (`model.eval()` in PyTorch) before serving produces incorrect predictions silently.

**Batch Size**
The number of training examples processed together before a weight update. Smaller batches produce noisier gradient estimates with a regularizing effect. Larger batches produce more accurate gradient estimates but often generalize worse and require more GPU memory. Doubling the batch size roughly doubles GPU memory consumption. The most common fix for a CUDA out-of-memory error during training is to halve the batch size.

**BentoML**
A model serving framework that provides abstractions for packaging models with their preprocessing logic, serving them via HTTP, and deploying to various targets. Sits above raw FastAPI in the abstraction stack. Useful when you need quick deployment without writing all serving infrastructure from scratch.

**Blue-Green Deployment**
A deployment strategy that maintains two identical production environments. At any point, one is live (blue) and one is idle (green). To release, you deploy to green, run tests, then switch traffic. If something fails, you switch back to blue. Less common in ML than canary rollouts because it requires maintaining two full serving environments simultaneously.

---

## C

**Calibration**
The degree to which a model's predicted probabilities reflect actual event frequencies. A perfectly calibrated model that predicts 70% probability for an event is correct approximately 70% of the time for those predictions. Uncalibrated models may be systematically overconfident or underconfident. Calibration matters whenever the raw probability is used as input to a downstream decision — risk scoring, threshold selection, or combining multiple model outputs. Assessed via reliability diagrams. Fixed via Platt scaling or isotonic regression post-training.

**Canary Deployment**
A deployment strategy that routes a small percentage of production traffic to a new model version while the remainder continues to the existing version. Traffic is incrementally shifted as confidence builds. The strategy is named after the mining practice of using canaries to detect toxic gases — a small exposure before full commitment. Standard progression: 5% → 25% → 50% → 100%, with evaluation at each stage. Rollback means changing the traffic split configuration, which should take under 30 seconds without a redeployment.

**Champion-Challenger**
The framing of production model deployment as a competition between the existing production model (champion) and a candidate new model (challenger). The challenger earns traffic only by demonstrating measurable improvement over the champion on held-out data. Multiple challengers can compete simultaneously. The champion is replaced only when a challenger demonstrably wins.

**Covariate Shift**
See *Data Drift*.

**Concept Drift**
A change in the statistical relationship between input features and the target variable — formally, P(Y|X) changes. Distinct from data drift, where the input distribution changes but the relationship is stable. Concept drift cannot be fixed by simply retraining on more recent data if the features themselves no longer capture the relevant patterns. Requires investigation of the feature set and potentially redesigning what the model is measuring.

**Continuous Training (CT)**
The practice of automatically retraining and redeploying models in response to triggers — time-based schedules, detected data drift, or degraded performance. The ML equivalent of continuous deployment in software engineering. Requires a complete automated pipeline from data validation through model evaluation to deployment, with a quality gate that prevents a worse model from reaching production.

**Cross-Entropy Loss**
The most common loss function for classification problems. Measures the divergence between the predicted probability distribution and the true distribution. For binary classification, reduces to: `-[y * log(p) + (1-y) * log(1-p)]`. Heavily penalizes confident wrong predictions — predicting 0.99 probability for the wrong class incurs much more loss than predicting 0.6.

---

## D

**Data Drift**
A change in the statistical distribution of input features between training time and serving time — formally, P(X) changes. The model-world relationship may still be valid, but the model is now operating on inputs it has rarely or never seen. Common cause: product changes, seasonality, user base expansion, upstream data pipeline changes. Detected via statistical tests (KS test, chi-squared) or PSI. Response: retrain with data that represents the current distribution.

**Data Lineage**
The documented history of how a dataset was produced — its source systems, transformations, validations, and derived datasets. Essential for debugging data quality issues, auditing model behavior, and reproducing historical model states. In practice, most ML teams have incomplete data lineage and discover this only during incident investigation.

**Data Parallelism**
A distributed training strategy where the full model is replicated on each compute device, but training data is split across devices. Each device computes gradients on its data shard; gradients are then synchronized across devices (averaged) before weights are updated. The most common form of distributed training. Effective when the model fits in a single device's memory and the bottleneck is computation time rather than memory.

**Data Poisoning**
A category of attack against ML systems where an adversary injects malicious examples into the training data to corrupt model behavior. Can be targeted (causing specific misclassifications) or broad (degrading overall performance). Particularly relevant to systems that train on user-labeled data or data scraped from the internet.

**Data Versioning**
Tracking which specific version of a dataset was used to train each model. Without data versioning, you cannot reproduce a historical model even if you have the code and hyperparameters. Implemented using tools like DVC, which stores lightweight pointer files in Git while actual data resides in object storage.

**DeepSpeed**
A distributed training library from Microsoft that implements the ZeRO (Zero Redundancy Optimizer) family of memory optimization techniques. ZeRO eliminates the redundancy inherent in data parallel training by partitioning optimizer states, gradients, and model parameters across devices. Enables training models that would not fit in the aggregate GPU memory of a cluster using standard data parallelism.

**Differential Privacy**
A mathematical framework for training models that provides a formal guarantee that the model cannot be used to reconstruct information about specific training examples. Achieved by adding calibrated noise to the training process. The privacy budget (epsilon) quantifies the privacy guarantee — smaller epsilon means stronger privacy with some cost to model utility. Used in federated learning and any context where training data is sensitive.

**Distillation**
See *Knowledge Distillation*.

**Dropout**
A regularization technique where, during each training forward pass, a random fraction of neuron activations are set to zero. Forces the network to learn redundant representations and prevents co-adaptation of neurons. The dropout rate (e.g., 0.3) is a hyperparameter. Dropout is active only during training — during inference, all neurons are active and outputs are scaled. Failing to disable dropout at inference time is a common production bug that causes non-deterministic predictions.

**Drift**
The general term for any change in the statistical properties of an ML system's inputs, outputs, or underlying relationships over time. Three distinct types with different root causes and required responses: data drift (input distribution changes), concept drift (input-output relationship changes), and label drift (target distribution changes). See individual entries for each type.

**DVC (Data Version Control)**
A version control system for large files — primarily datasets, models, and pipeline artifacts. Integrates with Git: DVC stores lightweight pointer files in Git while actual data is stored in remote storage (S3, GCS, local). Enables reproducibility by allowing any historical state (code + data + model) to be reconstructed by checking out a Git commit and running `dvc checkout`.

---

## E

**Early Stopping**
A training technique that monitors validation loss during training and halts training when validation loss stops improving. Prevents overfitting by stopping before the model begins memorizing training noise. Requires a validation set held out from training, a patience parameter (how many epochs to wait for improvement before stopping), and checkpointing to save the best model state before performance degrades.

**Embedding**
A dense numerical vector representation of an entity — a word, a user, a product, an image. Learned during training such that similar entities have similar vector representations. Embeddings reduce high-dimensional sparse inputs (a vocabulary of 100,000 words) to dense low-dimensional representations (a 300-dimensional vector) and capture semantic relationships that one-hot encodings cannot. Two embeddings that are close in vector space represent entities the model has learned are semantically similar.

**Endpoint**
In the context of model serving, an HTTP or gRPC API that accepts feature vectors and returns predictions. May serve a single model or route requests across multiple model versions. Managed endpoints (SageMaker Endpoints, Vertex AI Endpoints) abstract infrastructure management; self-managed endpoints (FastAPI on Kubernetes) require explicit infrastructure configuration.

**Entropy**
A measure of uncertainty or disorder in a probability distribution. In ML, appears in cross-entropy loss, information gain in decision trees, and as a diagnostic metric for model confidence distributions. A model predicting very high entropy (close to uniform probability across classes) on most inputs is uncertain — this can indicate distribution shift or a model that has learned poorly.

**Epoch**
One complete pass through the entire training dataset. Training typically runs for multiple epochs. The number of epochs is a hyperparameter, often replaced in practice by early stopping criteria.

**Evidently AI**
An open-source library for ML monitoring and data validation. Generates reports and test suites comparing reference datasets to current datasets, covering data drift, data quality, model performance, and prediction drift. The standard tool for implementing drift detection pipelines in production without building statistical testing infrastructure from scratch.

**Experiment**
In MLflow and most tracking systems, a named container for related runs. A single experiment might contain hundreds of training runs representing different hyperparameter configurations, dataset versions, or architectural variations. Experiments enable comparison across runs and provide the organizational structure for tracking iterative model development.

---

## F

**F1 Score**
The harmonic mean of precision and recall: `2 * (precision * recall) / (precision + recall)`. Provides a single number that balances both metrics. The harmonic mean specifically penalizes extreme imbalance — a model with perfect precision and zero recall has an F1 of zero. Appropriate when both false positives and false negatives have meaningful costs. For cases where one type of error is more costly, use F-beta.

**F-Beta Score**
A generalization of F1 that allows weighting precision and recall differently. Beta controls the trade-off: beta > 1 weights recall more heavily (use when false negatives are more costly), beta < 1 weights precision more heavily (use when false positives are more costly). F2 score gives recall twice the weight of precision; F0.5 gives precision twice the weight.

**Feature**
Any input variable used by a model to make predictions. May be a raw data field, a transformed version of a raw field, or an aggregate computed over a window of time. The quality and relevance of features is the dominant factor in model performance for most production problems — model architecture and hyperparameter tuning matter much less than having the right features.

**Feature Drift**
See *Data Drift*.

**Feature Engineering**
The process of transforming raw data into representations that models can use effectively. Includes normalization, encoding categorical variables, creating aggregate statistics over time windows, handling missing values, and creating interaction terms. Feature engineering is where domain knowledge matters most and where the most impactful work in tabular ML happens.

**Feature Importance**
A measure of how much each input feature contributes to a model's predictions. For tree-based models, computed from how frequently and effectively a feature is used in splits. For neural networks, typically computed via gradient-based methods or SHAP. Used for model debugging, feature selection, and detecting when a model is relying on spurious correlations.

**Feature Leakage**
See *Data Leakage*.

**Feature Store**
A system that centralizes the definition, computation, storage, and serving of features for ML models. Solves training-serving skew by ensuring that features are computed identically during training and serving. Provides an offline store (historical data for training) and an online store (current values for real-time serving). The two most common open-source implementations are Feast and Hopsworks.

**Feature Store Materialization**
The process of computing features from raw data sources and writing the results to the online store so they are available for real-time serving. Run on a schedule — hourly, for example — to keep online feature values current. The staleness of materialized features is a design parameter determined by how quickly the underlying data changes and how fresh predictions need to be.

**Feast**
An open-source feature store that manages feature definitions, computes features from data sources, and serves them for both training and inference. Supports multiple offline backends (Parquet, BigQuery, Redshift) and online backends (Redis, DynamoDB). The feature registry tracks what features exist and how they are defined.

**Federated Learning**
A training paradigm where the model trains across multiple devices or data silos without centralizing the data. Each participant trains locally on their own data, shares only model updates (gradients), and a central server aggregates updates. The raw training data never leaves its origin. Used in mobile applications where user data should not be uploaded, and in healthcare and finance where data cannot be combined across institutions for regulatory reasons.

**Fine-tuning**
Continuing to train a pretrained model on a new, typically smaller dataset for a specific task. The pretrained model provides initialization from a large general training run; fine-tuning adapts it to the target task. Dramatically reduces the data and compute required compared to training from scratch. The standard approach for using large pretrained models (BERT, LLaMA, etc.) in production applications.

**Focal Loss**
A modification of cross-entropy loss designed for severely imbalanced classification problems. Reduces the loss contribution from easy examples (predictions the model is already confident about) so that training focuses disproportionately on hard examples and rare classes. Widely used in object detection and fraud detection where positive examples may be less than 1% of the training set.

---

## G

**Gradient**
The vector of partial derivatives of the loss function with respect to each model parameter. Points in the direction of steepest ascent of the loss. Gradient descent moves in the opposite direction — toward lower loss. The gradient is computed via backpropagation and used by the optimizer to update model weights.

**Gradient Clipping**
Scaling down the gradient when its norm exceeds a threshold before applying it to update weights. Prevents exploding gradients — situations where gradient values grow exponentially through layers of a deep network and cause weight updates that destabilize training. Standard practice when training recurrent networks and transformers.

**Gradient Descent**
The family of optimization algorithms that update model parameters by moving them in the direction opposite to the gradient of the loss function. Stochastic gradient descent (SGD) computes the gradient on a single sample or small batch; this noisiness has a regularizing effect but requires careful learning rate tuning. See also *Adam*, *AdamW*.

**Great Expectations**
An open-source Python library for defining, documenting, and validating data quality expectations. Expectations are assertions about data properties — column nullability, value ranges, distribution statistics, referential integrity — that are checked automatically when new data arrives. Integrates into data pipelines as a validation gate that can halt processing when data does not meet quality requirements.

---

## H

**Holdout Set**
See *Test Set*.

**Hugging Face**
A platform and library ecosystem for transformer-based models. The `transformers` library provides a standard interface for loading, fine-tuning, and running inference with thousands of pretrained models. The Hub hosts models, datasets, and spaces. The `safetensors` format they developed is the standard safe serialization format for neural network weights, replacing pickle-based formats.

**Hyperparameter**
A configuration value that is set before training begins and is not updated by the training process. Learning rate, batch size, number of layers, dropout rate, and regularization strength are all hyperparameters. Distinct from model parameters (weights), which are learned during training. Hyperparameter values have a significant effect on model performance and must be logged with every training run for reproducibility.

**Hyperparameter Search**
The process of finding hyperparameter values that produce good model performance. Grid search evaluates all combinations of specified values. Random search samples randomly from distributions over values. Bayesian optimization builds a probabilistic model of performance as a function of hyperparameters and selects candidates to evaluate that are most likely to improve. Modern tools like Ray Tune implement adaptive scheduling that terminates poorly performing trials early.

---

## I

**Inference**
The process of using a trained model to make predictions on new data. Also called serving or scoring. Distinct from training, which updates model weights. The computational requirements for inference are typically much lower than training but must meet latency requirements that training does not.

**Inference Latency**
The wall-clock time between receiving a prediction request and returning the result. Measured at percentile levels (P50, P95, P99) rather than as an average, because averages obscure tail latency that affects user experience. P99 latency of 500ms means 1% of requests take longer than 500ms. Production SLAs are typically defined at P99.

---

## K

**KL Divergence (Kullback-Leibler Divergence)**
A measure of how much one probability distribution differs from another. In ML, used to measure distribution shift between training and production data as a drift metric, and as a loss component in variational autoencoders. Not symmetric: KL(P||Q) ≠ KL(Q||P). The Jensen-Shannon divergence is the symmetric version.

**Knowledge Distillation**
A model compression technique where a smaller model (student) is trained to mimic a larger model (teacher). The student learns not just from ground truth labels but from the teacher's predicted probability distributions, which contain richer information than hard labels. A teacher predicting 92% class A, 7% class B, 1% class C encodes more information than the hard label "class A". The student trained on these soft targets learns more efficiently and often outperforms a student trained on hard labels alone.

**KubeFlow Pipelines (KFP)**
A Kubernetes-native ML pipeline framework where each pipeline step runs in an isolated container with its own resource allocation. Enables training jobs to request specific GPU configurations, memory, and CPU independently of other pipeline steps. Built on top of Argo Workflows. The standard orchestration layer for enterprise ML platforms on Kubernetes.

---

## L

**Label Drift**
A change in the distribution of the target variable over time — P(Y) changes. If a fraud detection model was trained when 1% of transactions were fraudulent and the current fraud rate is 0.1%, the model's base predictions will be poorly calibrated for the current environment. Response: adjust class weights and recalibrate decision thresholds.

**Label Leakage**
See *Data Leakage*.

**Latency**
See *Inference Latency*.

**Learning Rate**
The scalar that determines how much model weights are updated in response to the computed gradient. Too high: weight updates are large, training is unstable, loss may diverge. Too low: weight updates are small, training takes prohibitively long or converges to a poor solution. The most sensitive hyperparameter in neural network training. Learning rate schedules — which change the learning rate during training — often improve convergence.

**LIME (Local Interpretable Model-agnostic Explanations)**
A model explanation technique that approximates the behavior of a black-box model locally around a specific prediction using a simpler, interpretable model. Creates perturbed versions of the input, runs them through the model, and fits a linear model to the results. Non-deterministic and approximate. Useful for models where SHAP is not applicable (e.g., some neural network architectures). See also *SHAP*.

**LoRA (Low-Rank Adaptation)**
A parameter-efficient fine-tuning technique for large models. Instead of updating all model parameters during fine-tuning, LoRA inserts small trainable matrices (adapters) alongside frozen base model weights. The total number of trainable parameters is reduced by 99%+ compared to full fine-tuning, making fine-tuning of large language models feasible on modest hardware. QLoRA combines LoRA with 4-bit quantization of the base model, enabling 7B parameter model fine-tuning on a single consumer GPU.

**Loss Function**
See *Loss*.

**Loss**
A scalar value that measures how wrong the model's predictions are on the training data. The training process minimizes this value. The choice of loss function encodes what "wrong" means for a given problem — mean squared error treats large errors as proportionally worse than small ones; cross-entropy heavily penalizes confident wrong predictions; focal loss focuses training on hard examples. The loss function is one of the most consequential design decisions in ML.

---

## M

**MAE (Mean Absolute Error)**
The average of the absolute differences between predictions and actual values. Measured in the same units as the target variable. Less sensitive to outliers than RMSE because errors are not squared. Use when all error magnitudes are equally costly.

**Materialization**
See *Feature Store Materialization*.

**MLflow**
An open-source platform for the ML lifecycle: experiment tracking, model packaging, model registry, and model serving. The most widely deployed experiment tracking solution in production ML. Tracks runs with parameters, metrics, and artifacts; provides a model registry for managing model versions through staging, production, and archived stages; supports multiple model flavors (scikit-learn, PyTorch, TensorFlow, ONNX).

**Model Card**
A short document that accompanies a deployed model describing its intended use, training data, performance characteristics (disaggregated by relevant demographic groups), known limitations, and contact information for concerns. Required by the EU AI Act for high-risk AI systems. Introduced by Google researchers in 2018 as a standard for model transparency.

**Model Drift**
Degradation in model performance over time, which may be caused by data drift, concept drift, or upstream system changes rather than any problem with the model itself. Detected by monitoring model predictions and, where ground truth is available, model accuracy metrics in production.

**Model Parallelism**
A distributed training strategy where different parts of the model are placed on different devices. Used when the model is too large to fit on a single device. Tensor parallelism splits individual weight matrices; pipeline parallelism assigns different layers to different devices. Contrasted with data parallelism, where the full model is replicated and data is split.

**Model Registry**
A versioned store for trained model artifacts with metadata about training provenance, evaluation metrics, and deployment status. Provides a structured lifecycle (staging, production, archived) and serves as the single source of truth for what model is in production and how it was produced. MLflow Model Registry and W&B Artifacts are the most common implementations.

**MSE (Mean Squared Error)**
The average of the squared differences between predictions and actual values. Squaring errors makes large errors disproportionately costly. Not in the same units as the target variable (use RMSE for interpretable units). The standard loss function for regression problems where large errors are particularly costly.

---

## N

**NaN Loss**
A training failure mode where the loss becomes not-a-number (NaN), typically cascading to NaN gradients and NaN weights, halting all learning. Common causes: learning rate too high (weight updates overshoot and produce infinite values), NaN or Inf values in training data, numerical instability in a custom loss function (e.g., `log(0)`). Diagnosis: add data validation before training, reduce learning rate by 10x, add gradient clipping.

**NDCG (Normalized Discounted Cumulative Gain)**
A ranking quality metric that measures whether relevant items appear near the top of a ranked list. Items at higher ranks receive more weight — the "discount." Normalized so that scores are comparable across queries of different lengths. NDCG@K evaluates only the top K positions. Standard metric for search ranking and recommendation evaluation.

---

## O

**Offline Evaluation**
Measuring model performance on a held-out dataset before deployment. Provides a controlled, reproducible measure of model quality but is only as reliable as the held-out dataset is representative of real production traffic. Online and offline metrics frequently diverge — a model that performs better offline may perform worse in production if the test set does not represent current user behavior.

**Online Learning**
A training paradigm where the model updates continuously as new data arrives, rather than in discrete retraining cycles. Requires a short feedback loop and ground truth that arrives quickly. The model state at any point depends on the exact sequence of training examples seen, making debugging and reproducibility difficult. Appropriate for rapidly changing distributions; not appropriate for regulated contexts requiring auditable, stable model behavior.

**ONNX (Open Neural Network Exchange)**
A standardized format for representing trained ML models, independent of the framework used for training. Enables training in PyTorch and serving with ONNX Runtime, which supports optimized execution across CPU, GPU, and specialized hardware without the overhead of the training framework. The standard intermediate format for the PyTorch → ONNX → TensorRT production optimization pipeline.

**Overfitting**
A condition where a model performs well on training data but poorly on held-out data. The model has learned to memorize the training examples, including their noise, rather than learning generalizable patterns. Signal: training loss much lower than validation loss. Response: more training data, stronger regularization (dropout, L2), simpler model architecture, early stopping.

---

## P

**P99 Latency**
The latency at the 99th percentile — the value below which 99% of request latencies fall. Production latency SLAs are typically specified at P95 or P99 rather than as averages because averages obscure the tail behavior that affects the worst-served users. A system with average latency of 50ms and P99 latency of 2000ms is not performing acceptably for 1% of users.

**Parameter**
A learned numerical value in a model — the weights and biases updated during training. Distinct from hyperparameters, which are set before training. A model is fully described by its architecture and its parameter values. The number of parameters is a rough proxy for model capacity.

**Pipeline**
In ML, any sequence of transformations applied to data or models. May refer to a preprocessing pipeline (feature engineering steps), a training pipeline (data loading, training, evaluation, registration), or a serving pipeline (request validation, feature retrieval, inference, response formatting). Treating each stage as explicit and composable makes pipelines testable, reproducible, and maintainable.

**Point-in-Time Correct Features**
Feature values retrieved as they existed at a specific historical timestamp, rather than their current values. Essential for training data preparation in time-series ML problems to prevent data leakage. If you are training a model to predict whether a loan will default, you must use the credit score as it existed when the loan was issued — not today's credit score. Feature stores implement point-in-time correct retrieval.

**PR-AUC (Precision-Recall Area Under the Curve)**
The area under the precision-recall curve across all possible decision thresholds. More informative than ROC-AUC for imbalanced classification problems because it focuses on the minority class. A model can have a high ROC-AUC on a heavily imbalanced dataset while having a poor PR-AUC — the latter better reflects actual utility on the problem that matters.

**Precision**
The fraction of positive predictions that were correct: `TP / (TP + FP)`. Answers: "When the model predicts fraud, how often is it actually fraud?" High precision means few false alarms. The cost of low precision is wasted investigation effort and, in customer-facing systems, incorrectly blocking legitimate users. See also *Recall*.

**PSI (Population Stability Index)**
A metric measuring the statistical difference between two distributions, widely used in financial services ML for detecting input feature drift. PSI < 0.1 indicates no significant drift; 0.1 to 0.2 indicates moderate drift warranting investigation; above 0.2 indicates significant drift and is a standard trigger for retraining. Computed by comparing the bucket-wise distributions of the training population and current production population.

---

## Q

**Quantization**
Reducing the numerical precision of model weights and activations to decrease model size and increase inference speed. FP32 (4 bytes per value) → FP16 (2 bytes) → INT8 (1 byte) → INT4 (0.5 bytes). Each step roughly halves memory requirements and can proportionally increase throughput on hardware that supports the lower precision. Post-training quantization applies after training without modification; quantization-aware training simulates quantization during training to minimize accuracy loss.

---

## R

**RAG (Retrieval-Augmented Generation)**
An architecture for LLM applications that augments the model's context with information retrieved from an external knowledge base at inference time. The query is embedded and used to retrieve semantically relevant documents from a vector database; the retrieved documents are injected into the prompt before generation. Allows the model's outputs to be grounded in current, specific information without the cost of retraining or fine-tuning.

**Ray**
A distributed computing framework for Python. Provides primitives for distributed function execution (Ray Core), distributed ML training (Ray Train), distributed hyperparameter search (Ray Tune), and distributed model serving (Ray Serve). More general than training-specific frameworks like DeepSpeed — useful across the full ML lifecycle.

**Recall**
The fraction of actual positive cases that the model correctly identified: `TP / (TP + FN)`. Answers: "What fraction of actual fraud cases did the model catch?" High recall means few missed positives. The cost of low recall is the events that slip through undetected. The fundamental tradeoff between precision and recall requires a business decision about which type of error is more costly.

**Regularization**
Techniques that reduce overfitting by penalizing model complexity. L2 regularization (weight decay) penalizes large weights. L1 regularization (lasso) drives some weights to exactly zero, producing sparse models. Dropout randomly deactivates neurons during training. Early stopping prevents the model from training until it memorizes the training set. All reduce generalization error at the cost of some training accuracy.

**RMSE (Root Mean Squared Error)**
The square root of mean squared error. In the same units as the target variable, unlike MSE. Sensitive to outliers because errors are squared before averaging. Standard for regression evaluation when large errors are more costly than proportionally many small errors.

**ROC-AUC**
The area under the receiver operating characteristic curve — a plot of true positive rate against false positive rate across all possible decision thresholds. Equals the probability that the model assigns a higher score to a randomly chosen positive example than to a randomly chosen negative example. Threshold-independent, making it useful for comparing models. Less informative than PR-AUC for severely imbalanced datasets.

**Run**
In experiment tracking, a single execution of a training script with a specific configuration. A run records parameters, metrics over time, artifacts, and system metadata. Multiple runs within an experiment represent different attempts to solve the same problem.

---

## S

**SafeTensors**
A serialization format for neural network weights developed by Hugging Face. Unlike pickle-based formats, SafeTensors cannot execute arbitrary code when loaded, making it safe to load tensors from untrusted sources. Replaced `.pt` files and pickle-based formats as the standard for distributing model weights. The default format for models on the Hugging Face Hub.

**SHAP (SHapley Additive exPlanations)**
A model explanation framework based on game-theoretic Shapley values. Assigns each feature a value representing its contribution to a specific prediction, decomposing the prediction into a sum of per-feature contributions. The contributions sum to the difference between the prediction and the model's average prediction. Provides both local explanations (why was this specific prediction made) and global explanations (which features matter most overall). `TreeExplainer` provides exact, fast computation for tree-based models. The industry standard for production model explainability.

**Shadow Deployment**
A deployment configuration where a new model runs on production traffic alongside the existing model, but its predictions are logged and never served to users. The existing model's predictions are served. Allows the new model to be evaluated on real traffic with zero user risk. Reveals engineering problems — latency regressions, memory issues, edge case failures — that held-out test sets cannot expose.

**Skew**
See *Training-Serving Skew*.

**Standardization**
A preprocessing transformation that scales a feature to have zero mean and unit variance: `(x - mean) / std`. The mean and standard deviation must be computed on training data only and applied to both training and serving data. Essential for models that use distance metrics or gradient-based optimization — without standardization, features with large numerical ranges dominate gradients. See also *Training-Serving Skew*.

---

## T

**TensorRT**
NVIDIA's inference optimization library. Compiles ONNX models into hardware-optimized execution engines for NVIDIA GPUs. Applies fusion, precision reduction (FP16, INT8), and kernel selection to maximize throughput on the target hardware. Provides 3–10x inference speedup over the original training framework on compatible hardware. The last step in the standard PyTorch → ONNX → TensorRT optimization pipeline.

**Test Set**
A held-out subset of labeled data used exclusively for final model evaluation. Never used to make any training or hyperparameter decisions. Evaluating a model on its test set multiple times and making decisions based on those evaluations converts the test set into a validation set — you no longer have an honest estimate of generalization performance.

**Training-Serving Skew**
Discrepancies between the data a model was trained on and the data it receives during serving, caused by differences in how features are computed in the training pipeline versus the serving pipeline. The same conceptual feature computed through different code paths or with different parameters produces different numerical values. The model receives inputs it was not trained on; predictions degrade silently. Prevented by using a feature store with a single feature definition used in both pipelines.

**Transfer Learning**
Using a model trained on one task as the starting point for training on a different task. The pretrained model has learned useful representations that generalize across tasks. Fine-tuning adapts these representations to the new task with less data and compute than training from scratch. The dominant paradigm for using large pretrained models (BERT, ResNet, LLaMA) in production applications.

**Triton Inference Server**
NVIDIA's production model serving platform. Hosts models from multiple frameworks (ONNX, TensorRT, PyTorch, TensorFlow, scikit-learn) through a unified API. Key capabilities: dynamic batching (automatically batches individual requests to improve GPU utilization), concurrent model execution (multiple models running simultaneously on the same GPU), ensemble pipelines (model composition in a single API call), and a model repository pattern (deploy new model versions by adding files without restart).

---

## U

**Underfitting**
A condition where a model performs poorly on both training and held-out data. The model has insufficient capacity to capture the patterns in the data. Signal: training loss and validation loss both remain high and similar. Response: more complex model architecture, better feature engineering, less regularization, more training time.

---

## V

**Validation Set**
A held-out subset used during training to monitor generalization performance, tune hyperparameters, and make early stopping decisions. Distinct from the test set, which is held out until final evaluation. Because validation set performance influences training decisions (hyperparameter selection, architecture choices), the validation set has indirect influence on the model — it is not an honest estimate of generalization performance. The test set exists for that purpose.

**vLLM**
A high-throughput inference engine for large language models. Implements PagedAttention, a memory management algorithm that treats the KV cache like virtual memory in an operating system. Enables significantly higher throughput than naive implementations by eliminating memory fragmentation and waste in KV cache allocation. The standard serving infrastructure for self-hosted LLM deployments.

---

## W

**W&B (Weights & Biases)**
An experiment tracking platform with stronger visualization capabilities than MLflow, particularly for comparing runs and analyzing model behavior. Hosted service with a free tier; self-hosting requires more infrastructure than MLflow. Preferred by research teams for its richer UI; MLflow preferred in enterprise settings for its open-source self-hosted simplicity.

**Weight Decay**
See *L2 Regularization*.

---

## Z

**ZeRO (Zero Redundancy Optimizer)**
A family of memory optimization techniques implemented in DeepSpeed that eliminate the memory redundancy inherent in data parallel training. Standard data parallelism replicates the full model, gradients, and optimizer states on every device. ZeRO Stage 1 partitions optimizer states; Stage 2 also partitions gradients; Stage 3 also partitions model parameters. Stage 3 with 64 devices provides 64x memory reduction compared to standard data parallelism, enabling training of models that would not fit in aggregate GPU memory.
