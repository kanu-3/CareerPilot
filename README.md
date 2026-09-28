# CareerPilot

CareerPilot is an AI-powered personal career agent built with **FastAPI, LangGraph, LangChain, RAG, Supabase/pgvector, and a local LLM**.

The backend agent and API functionality are currently the primary working components. **Use the FastAPI Swagger UI to test the complete application.** The Streamlit frontend is currently experimental and is not the recommended interface for testing the agent.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/kanu-3/CareerPilot.git
cd CareerPilot
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Configure the required services, including Supabase and other dependencies used by the project.

**Do not commit `.env` or any credentials/API keys to GitHub.**

---

## Local LLM Setup

CareerPilot currently uses **Qwen through Ollama**.

Install Ollama and make sure the Ollama service is running.

The LLM integration is located at:

```text
backend/
└── llm/
    └── qwen.py
```

The current configuration is:

```python
OLLAMA_URL = "http://localhost:11434"
LLM_MODEL = "qwen2.5vl:3b"
```

Pull the model:

```bash
ollama pull qwen2.5vl:3b
```

### Using another Ollama model

You can replace:

```python
LLM_MODEL = "qwen2.5vl:3b"
```

with another model available through Ollama.

For example:

```python
LLM_MODEL = "llama3.2:3b"
```

If your Ollama server is running at a different address, update:

```python
OLLAMA_URL = "http://localhost:11434"
```

The current `qwen.py` implementation expects an **Ollama-compatible API**. To use a completely different LLM provider, replace the LLM implementation accordingly.

---

# Running the Backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Check the backend:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# Using Swagger

Swagger is the recommended way to interact with and test the current version of CareerPilot.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger exposes **all active backend endpoints**, including the agent, profile, and approval functionality.

You can expand each endpoint, select **Try it out**, provide the required request data, and execute it directly from the browser.

## Main API areas

### Agent

The agent endpoint is:

```text
POST /agent/run
```

Example request:

```json
{
  "user_id": 1,
  "job_id": 1,
  "request": "Analyze my fit for this job and create a learning path for my skill gaps."
}
```

The agent can use the user's profile, skills, job information, retrieved knowledge, memory, and available tools to determine the appropriate workflow.

### Profile

The profile endpoints allow you to work with the user's career/profile information.

Use the available **Profile** endpoints in Swagger to create, retrieve, or update profile-related data according to their request schemas.

### Approvals

The approval endpoints handle actions that require human confirmation.

```text
POST /approvals/{approval_id}/approve
POST /approvals/{approval_id}/reject
POST /approvals/{approval_id}/resume
```

Use the approval ID returned by the agent when an action requires human intervention.

---

# What the Agent Does

CareerPilot is designed as an agentic career assistant rather than a simple chatbot.

Depending on the request, the agent can:

* Analyze job fit
* Identify skill gaps
* Create personalized learning paths
* Recommend learning actions
* Work with user profile information
* Use job and career context
* Retrieve relevant information through RAG
* Use career, job, and learning tools
* Update relevant information
* Execute actions that do not require explicit approval
* Pause before consequential actions
* Request human approval
* Resume execution after approval

For example:

```text
User:
"Analyze my fit for this job and create a learning path."

        ↓

Agent analyzes profile + job

        ↓

Identifies skill gaps

        ↓

Creates learning path

        ↓

Returns result
```

For a consequential action:

```text
User:
"Submit my application for this job."

        ↓

Agent determines that approval is required

        ↓

Approval request created

        ↓

User reviews the action

        ├── Reject
        │     ↓
        │    Stop
        │
        └── Approve
              ↓
           Resume
              ↓
           Execute
```

This means the agent can automate appropriate tasks while keeping consequential actions under explicit user control.

---

# Human-in-the-Loop

CareerPilot uses a human-in-the-loop approval mechanism for consequential actions.

For example, an action such as **submitting a job application** requires user approval before execution.

When approval is required, the agent returns an approval ID.

The user can then:

### Approve

```text
POST /approvals/{approval_id}/approve
```

### Reject

```text
POST /approvals/{approval_id}/reject
```

### Resume an approved action

```text
POST /approvals/{approval_id}/resume
```

The approval flow allows the agent to pause its workflow, wait for a human decision, and continue execution only after approval.

---

# High-Level Architecture

```text
                         USER
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    Profile Form      Resume Upload    Other Documents
          │                │                │
          │                ▼                │
          │         Parser / Extractor      │
          │                │                │
          └────────────┬───┴────────────────┘
                       ▼
                PROFILE INGESTION
                       │
                Human Confirmation
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   STRUCTURED DATA           UNSTRUCTURED DATA
          │                         │
          ▼                         ▼
     PostgreSQL               Document Store
                                    │
                                 Chunking
                                    │
                                 Embeddings
                                    │
                                    ▼
                                 Vector DB
          │                         │
          └────────────┬────────────┘
                       ▼
                KNOWLEDGE LAYER
                       │
                       ▼
                   RETRIEVER
                       │
                       ▼
                LANGGRAPH AGENT
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
          Planner   Decision    Memory
             │         │         │
             └─────────┼─────────┘
                       ▼
                     TOOLS
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Job Tools   Career Tools  Learning Tools
          │            │            │
          └────────────┼────────────┘
                       ▼
                APPROVAL GATEWAY
                       │
                       ▼
                   EXECUTION
                       │
                       ▼
                   AUDIT LOG
```

---

# Current Interface Status

The **FastAPI backend, API endpoints, and LangGraph agent are the primary working components**.

For the current version, use Swagger:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface exposes the complete set of active API endpoints and is the recommended way to test the backend.

The Streamlit frontend is currently experimental and may experience additional response latency, so it is **not the recommended interface for testing the current agent workflow**.
