# AI Communication Lab

AI Communication Lab is a local-first evaluation engine for analyzing written communication using large language models.

This project started from a personal goal: improving my own written communication. Instead of relying on cloud-based tools, I wanted something structured, private, and fully under my control. Building the system also helped me understand how to integrate probabilistic LLM output into deterministic backend systems.

I used ChatGPT as a technical discussion partner while thinking through architecture decisions, schema enforcement, validation layers, and failure handling. The goal was not to auto-generate code, but to reason more rigorously about system design and trade-offs.

This is not a chatbot. It is a structured evaluation pipeline.

---

## What This Project Does

Given an input text, the system:

1. Builds a structured evaluation prompt
2. Sends it to a local Ollama model (`qwen2.5:7b-instruct`)
3. Enforces strict JSON output
4. Cleans minor formatting issues (e.g. markdown fences)
5. Validates the result using Pydantic
6. Computes a deterministic weighted score
7. Persists the evaluation in SQLite
8. Emits execution telemetry using Logfire

The output includes:

- Mode-specific dimension scores
- Strengths
- Weaknesses
- Rewrite suggestion (what to improve)
- Rewrite example (an improved version of the text)

All evaluation runs locally. No external APIs are required.

---

## Design Principles

- Strict schema validation (Pydantic)
- Deterministic scoring defines the canonical rubric
- Limited sanitization (format cleanup only, no silent mutation)
- Clear separation of concerns
- Observability isolated from business logic
- Fail fast on invalid output

Correctness comes before convenience.

---

## Project Structure

```commandline
├── app
│   ├── __init__.py
│   ├── __pycache__
│   ├── llm_engine.py
│   ├── main.py
│   ├── models.py
│   ├── observability.py
│   ├── prompts.py
│   ├── scoring.py
│   └── storage.py
├── database
│   └── evaluations.db
├── README.md
├── requirements.txt
├── tests
│   ├── __pycache__
│   ├── test_scoring.py
│   └── test_storage.py
```

### Responsibilities

- `prompts.py` — Prompt construction
- `llm_engine.py` — Ollama integration + sanitization
- `models.py` — Pydantic schemas
- `scoring.py` — Deterministic weighted scoring
- `storage.py` — SQLite persistence (SQLAlchemy)
- `observability.py` — Logging / tracing abstraction
- `main.py` — Pipeline orchestration

---

## Local LLM Setup (Ollama)

### 1. Install Ollama

https://ollama.com

### 2. Pull the Model

```bash
ollama pull qwen2.5:7b-instruct
```

### 3. Start the Ollama Server
In first terminal
```bash
ollama serve
```

### 4. Run model 
Another terminal
```bash
ollama run qwen2.5:7b-instruct
```

The application communicates with:
```curl
POST http://localhost:11434/api/generate
```


## Observability (Logfire)

The system uses Logfire for tracing and execution telemetry.

It captures:
	•	Function-level spans
	•	Success and failure events
	•	Execution time (latency)

Observability is implemented through a generic decorator so logging remains isolated from business logic.

Create free Account : https://logfire.dev

```bash
# install
pip install logfire
# auth
logfire auth
```

## Setup & Running the Project
```bash
# clone this repo
git clone <repo-url>
cd ai-communication-lab

# create python virtual env
python -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# Start Ollama (separate terminal)
ollama serve

#  Run the Evaluation Pipeline (separate terminal)
python

# then 
>>> from app.main import run_llm_pipeline
>>> run_llm_pipeline("This is sample text, you can add anything...")
```

The system will:
* 	Call the local model
* 	Validate the response
* 	Compute weighted score
* 	Store the result in SQLite
* 	Emit telemetry

## Running Tests
```bash
pytest
```

Tests currently cover:
* Deterministic scoring logic 
* rage persistence

#### SQLite is used for local persistence.