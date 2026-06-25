# 01 — LLMOps Complete Guide


## Prerequisites

**MLOps mastery:** Completed the core MLOps section of this guide. Understand experiment tracking, model serving, continuous training.

**LLM basics:** Have used ChatGPT or Claude. Know what a prompt is. Understand "tokens" and context windows.

**Required tools:** Python · Hugging Face account · Access to an LLM API (OpenAI, Anthropic, or open-source)

> LLMOps is MLOps extended for large language models. Every MLOps skill transfers directly. New capabilities are additive, not replacements.
> LLMOps is MLOps extended for large language models. Every MLOps skill transfers directly. New capabilities are additive, not replacements.

---

## MLOps → LLMOps: What Transfers Directly

| MLOps Skill | LLMOps Equivalent |
|---|---|
| Model Registry | Hugging Face Hub + version tags |
| Experiment Tracking | Fine-tuning run tracking (W&B, MLflow) |
| Model Serving | vLLM, TGI, Ollama for LLM inference |
| Drift Monitoring | Output quality monitoring (LLM-as-judge) |
| Feature Stores | Embedding stores + Vector databases |
| Canary Deployments | Prompt version A/B testing |
| CI/CD Pipelines | Evaluation pipelines (RAGAS, HELM) |
| Cost Optimization | Token cost management, KV-cache tuning |

---

## Layer 1 — Foundation Model Selection

### The Decision Matrix

```
Data sensitivity HIGH or scale VERY HIGH?
    → Self-host open-weight model (Llama 3, Mistral, Qwen)

Early product development, capability matters most?
    → Closed API (GPT-4, Claude, Gemini)

Medium scale, moderate sensitivity?
    → Managed open models (Together AI, Replicate, HF Endpoints)
```

### Open-Weight Model Comparison (2024)

| Model | Params | VRAM (INT4) | Strengths |
|---|---|---|---|
| Llama 3.1 8B | 8B | ~6 GB | Fast, general purpose |
| Llama 3.1 70B | 70B | ~40 GB | High quality, instruction following |
| Mistral 7B | 7B | ~5 GB | Fast, good for structured output |
| Qwen2.5 72B | 72B | ~40 GB | Excellent multilingual |
| Phi-3 Mini | 3.8B | ~3 GB | Runs on laptop, surprisingly capable |

---

## Layer 2 — RAG Architecture

RAG (Retrieval-Augmented Generation) is the dominant pattern for knowledge-intensive LLM applications. Instead of encoding all knowledge in model weights, you retrieve relevant context at inference time.

### Complete RAG Pipeline

```
User Query
    ↓
[1] Query Preprocessing
    - Clean input
    - Detect language
    - Classify intent
    ↓
[2] Query Embedding
    - Embed using same model as indexing
    - e.g., text-embedding-ada-002 or sentence-transformers
    ↓
[3] Hybrid Search (Vector + Keyword)
    - Vector similarity in Qdrant/Weaviate/Pinecone
    - Keyword search via BM25/Elasticsearch
    - Reciprocal Rank Fusion to combine results
    ↓
[4] Reranking
    - Cross-encoder reranks top-50 → top-5
    - Much more accurate than first-stage retrieval
    ↓
[5] Context Assembly
    - Format retrieved chunks
    - Inject into prompt template
    - Stay within context window budget
    ↓
[6] LLM Generation
    - Grounded in retrieved context
    - Citation tracking for faithfulness
    ↓
[7] Output Validation
    - Guardrails check
    - Citation verification
    - Safety filtering
```

### Implementation with Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

# Initialize
client = QdrantClient("localhost", port=6333)
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Create collection
client.create_collection(
    collection_name="knowledge_base",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Index documents
def index_documents(documents: list[dict]):
    """documents = [{"text": "...", "source": "doc.pdf", "page": 1}]"""
    embeddings = encoder.encode([d["text"] for d in documents])
    
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding.tolist(),
            payload=doc
        )
        for doc, embedding in zip(documents, embeddings)
    ]
    
    client.upsert(collection_name="knowledge_base", points=points)

# Retrieve at query time
def retrieve(query: str, top_k: int = 10) -> list[dict]:
    query_vector = encoder.encode(query).tolist()
    
    results = client.search(
        collection_name="knowledge_base",
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    
    return [
        {"text": r.payload["text"], "source": r.payload["source"], "score": r.score}
        for r in results
    ]

# RAG generation
def rag_generate(query: str, llm_client) -> dict:
    # Retrieve
    chunks = retrieve(query, top_k=10)
    
    # Rerank (optional but recommended)
    chunks = rerank(query, chunks, top_k=4)
    
    # Build context
    context = "\n\n".join([f"[{i+1}] {c['text']}" for i, c in enumerate(chunks)])
    
    # Generate
    prompt = f"""Answer the question based only on the provided context.
If the context doesn't contain the answer, say "I don't have information about this."

Context:
{context}

Question: {query}

Answer:"""
    
    response = llm_client.generate(prompt)
    
    return {
        "answer": response,
        "sources": [c["source"] for c in chunks],
        "retrieved_chunks": chunks
    }
```

### RAG Failure Modes

| Failure Mode | Cause | Fix |
|---|---|---|
| Retrieval failure | Wrong embedding space, poor chunking | Tune chunk size, try different embedding model |
| Context contamination | Retrieved contradictory information | Better deduplication, source filtering |
| Context overflow | Too many chunks exceed context window | Aggressive reranking, context compression |
| Semantic mismatch | Query and document use different terms | Query expansion, HyDE technique |
| Hallucination despite retrieval | Model ignores context | Stronger system prompt, smaller context window |

### Chunking Strategies

```python
# Strategy 1: Fixed size (simple, baseline)
def fixed_size_chunks(text: str, chunk_size: int = 512, overlap: int = 50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Strategy 2: Semantic chunking (better quality)
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]  # tries in order
)
chunks = splitter.split_text(document_text)

# Strategy 3: Hierarchical (best retrieval quality)
# Store both sentence-level and paragraph-level chunks
# Search sentence-level, return paragraph-level as context
```

---

## Layer 3 — Prompt Engineering and Management

### Prompt Versioning

Prompts are code. They must be version-controlled.

```python
# prompts/fraud_analysis_v3.py
SYSTEM_PROMPT = """You are a fraud analysis assistant for a financial institution.

Your role:
- Analyze transaction details and context provided
- Assess fraud risk based on patterns
- Provide clear reasoning for your assessment
- Never make definitive fraud determinations — only risk scores

Output format:
{
  "risk_score": 0-100,
  "risk_level": "low|medium|high|critical",
  "reasoning": "explanation",
  "recommended_action": "approve|review|decline"
}

Constraints:
- Base analysis only on provided data
- Never access external systems
- Flag if context seems insufficient for assessment
"""

VERSION = "3.0.0"
LAST_UPDATED = "2024-01-15"
CHANGELOG = "Added output format requirement, improved reasoning instruction"
```

```python
# Prompt registry
class PromptRegistry:
    def __init__(self):
        self.prompts = {}
    
    def register(self, name: str, version: str, prompt: str):
        if name not in self.prompts:
            self.prompts[name] = {}
        self.prompts[name][version] = prompt
    
    def get(self, name: str, version: str = "latest") -> str:
        if version == "latest":
            version = max(self.prompts[name].keys())
        return self.prompts[name][version]
    
    def get_active(self, name: str) -> str:
        """Get the A/B tested active version"""
        # Could use feature flags, config, or database
        active_version = config.get(f"prompts.{name}.active_version")
        return self.get(name, active_version)
```

### Prompt Injection Defense

```python
import re

class PromptSanitizer:
    # Patterns that indicate injection attempts
    INJECTION_PATTERNS = [
        r"ignore.{0,20}(previous|above|all).{0,20}instruction",
        r"(you are now|pretend you are|act as)",
        r"(reveal|show|print|output).{0,20}(system prompt|instructions)",
        r"(DAN|jailbreak|ignore constraints)",
        r"<!--.*-->",  # HTML comments
    ]
    
    def sanitize(self, user_input: str) -> str:
        """Check for injection patterns, raise if found."""
        lower = user_input.lower()
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, lower):
                raise ValueError(f"Potential prompt injection detected")
        return user_input
    
    def wrap_user_input(self, user_input: str) -> str:
        """Wrap user input to reduce injection risk."""
        return f"<user_input>{user_input}</user_input>"
```

---

## Layer 4 — Fine-Tuning with LoRA/QLoRA

### When to Fine-Tune

```
Fine-tune when:
  ✓ Need consistent output format/structure
  ✓ Have 500+ high-quality examples
  ✓ Need domain-specific knowledge/terminology
  ✓ Latency critical (shorter prompts possible)

Don't fine-tune when:
  ✗ Fewer than 500 good examples
  ✗ Need recent/updated knowledge (fine-tuning ≠ knowledge update)
  ✗ Good results achievable with prompting alone
  ✗ Budget/time constraints are tight
```

### QLoRA Fine-Tuning Pipeline

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from trl import SFTTrainer
import torch

# Load base model in 4-bit quantization (QLoRA)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    load_in_4bit=True,              # QLoRA: 4-bit base model
    bnb_4bit_quant_type="nf4",     # NormalFloat4 — better for LLMs
    bnb_4bit_compute_dtype=torch.float16,
    device_map="auto"
)

# Prepare model for k-bit training
model = prepare_model_for_kbit_training(model)

# Configure LoRA adapters
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                          # Rank: higher = more capacity, more memory
    lora_alpha=32,                 # Scaling factor
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.1,
    bias="none",
)

# Apply LoRA — only 0.1% of parameters are trainable!
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 8,033,669,120 (0.05%)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")

training_args = TrainingArguments(
    output_dir="./fine-tuned-model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=100,
    report_to="mlflow",            # Track in MLflow!
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    dataset_text_field="text",
    max_seq_length=2048,
)

trainer.train()

# Merge LoRA adapters into base model for serving
model = model.merge_and_unload()
model.save_pretrained("./merged-model")
```

---

## Layer 5 — LLM Observability

### Tracing with Langfuse

```python
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://your-langfuse.com"
)

@observe()
def rag_pipeline(query: str, user_id: str) -> dict:
    # Langfuse automatically traces this function
    
    langfuse_context.update_current_observation(
        input=query,
        metadata={"user_id": user_id}
    )
    
    # All nested calls are automatically traced
    chunks = retrieve(query)
    response = generate(query, chunks)
    
    langfuse_context.update_current_observation(
        output=response,
        usage={"input_tokens": 450, "output_tokens": 120},
        metadata={"retrieved_chunks": len(chunks)}
    )
    
    return response
```

### LLM-as-Judge Evaluation

```python
def evaluate_with_llm_judge(question: str, context: str, answer: str) -> dict:
    """Use a powerful LLM to evaluate another LLM's output."""
    
    evaluation_prompt = f"""Evaluate the following answer on three dimensions.
Score each from 1-5 and explain briefly.

Question: {question}
Context provided: {context}
Answer to evaluate: {answer}

Evaluate:
1. Faithfulness (1-5): Is the answer grounded in the provided context?
2. Relevance (1-5): Does the answer address the question?
3. Coherence (1-5): Is the answer logically sound and well-structured?

Respond in JSON: {{"faithfulness": X, "relevance": X, "coherence": X, "explanation": "..."}}"""

    result = judge_llm.generate(evaluation_prompt)
    scores = json.loads(result)
    
    # Alert if quality drops
    avg_score = (scores["faithfulness"] + scores["relevance"] + scores["coherence"]) / 3
    if avg_score < 3.5:
        alert(f"LLM output quality below threshold: {avg_score:.1f}")
    
    return scores
```

### RAGAS — Automated RAG Evaluation

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

dataset = {
    "question": questions,
    "answer": generated_answers,
    "contexts": retrieved_contexts,
    "ground_truth": reference_answers
}

results = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision]
)

print(results)
# faithfulness: 0.87
# answer_relevancy: 0.92
# context_precision: 0.78
```

---

## Layer 6 — LLM Cost Optimization

### Token Cost Reduction Strategies

```python
# Strategy 1: Prompt compression
# LLMLingua: compress prompts 3-5x with minimal quality loss
from llmlingua import PromptCompressor

compressor = PromptCompressor()
compressed = compressor.compress_prompt(
    original_prompt,
    rate=0.4,           # keep 40% of tokens
    force_tokens=["\n", "?"]  # always keep these
)
# Result: 60% fewer tokens, similar quality

# Strategy 2: Semantic caching
import hashlib
from redis import Redis

cache = Redis()

def cached_generate(prompt: str, ttl: int = 3600) -> str:
    cache_key = f"llm:{hashlib.sha256(prompt.encode()).hexdigest()}"
    
    cached = cache.get(cache_key)
    if cached:
        return cached.decode()
    
    response = llm.generate(prompt)
    cache.setex(cache_key, ttl, response)
    return response

# Strategy 3: Model routing
def route_to_model(query: str) -> str:
    complexity = classify_complexity(query)
    
    if complexity == "simple":
        return llama_8b.generate(query)    # cheap: $0.0002/1k tokens
    elif complexity == "medium":
        return llama_70b.generate(query)   # medium: $0.001/1k tokens
    else:
        return gpt4.generate(query)        # expensive: $0.03/1k tokens
```

---

## vLLM — High-Throughput LLM Serving

```bash
# Install
pip install vllm

# Serve Llama 3.1 8B
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Meta-Llama-3.1-8B-Instruct \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.90 \
    --max-model-len 8192 \
    --port 8000
```

```python
# Use OpenAI-compatible API
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")

response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Explain gradient descent"}],
    max_tokens=500,
    temperature=0.7
)
```

### vLLM Key Features

- **PagedAttention** — Manages KV-cache memory like OS virtual memory, 24x more efficient
- **Continuous batching** — Processes multiple requests simultaneously without padding waste
- **OpenAI API compatibility** — Drop-in replacement for OpenAI API calls
- **Quantization support** — AWQ, GPTQ, FP8 out of the box

---

## LLMOps Guardrails

```python
from guardrails import Guard
from guardrails.hub import ToxicLanguage, DetectPII, ProvideCorrectInformation

guard = Guard().use_many(
    ToxicLanguage(threshold=0.5, on_fail="exception"),
    DetectPII(pii_entities=["EMAIL", "PHONE", "SSN"], on_fail="fix"),
)

# Validate input before sending to LLM
@guard.parse(llm_output=False)
def validate_input(user_message: str):
    return user_message

# Validate LLM output before returning to user
@guard.parse(llm_output=True)
def validate_output(llm_response: str):
    return llm_response
```

---

**Previous:** [Platform Design](../advanced-specialized/05-platform-design.md) | **Next:** [Statistics →](../supporting-knowledge/01-statistics-for-mlops.md)
