# Autonomous Workday Reconciliation Agents

[![Vertex AI Agent Engine](https://img.shields.io/badge/Vertex%20AI-Agent%20Engine-blue.svg)](https://cloud.google.com/vertex-ai)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-Enabled-purple.svg)](https://github.com/astral-sh/uv)
[![A2A Protocol](https://img.shields.io/badge/A2A-Protocol%20Ready-green.svg)](https://a2a-protocol.org/)

An autonomous, decoupled dual-agent architecture designed to orchestrate the enterprise workday by planning priorities in the morning and reconciling completed work vs. open actions before sign-off.

---

## 📖 Executive Summary

On Glean and Google Cloud, the workday is orchestrated through two sovereign agent moments:

1. **☕ Morning Coffee (`morning-agent`)**:
   * **Trigger**: Runs daily at ~7:30 AM – 8:30 AM.
   * **Purpose**: Synthesizes recent collaboration activity, project deadlines, and high-signal meetings into a concise execution brief.
   * **Action**: Classifies focus blocks, filters meeting noise, and publishes the daily plan to cloud session memory.

2. **🍵 Afternoon Tea (`afternoon-agent`)**:
   * **Trigger**: Runs daily at ~3:30 PM – 5:00 PM.
   * **Purpose**: Evaluates intraday collaboration channels (Slack, Gmail, Zoom transcripts) against the morning plan.
   * **Action**: Reconciles closed vs. open tasks, applies strict ownership filtering (*"ball in user's court"*), deduplicates items across channels, and drafts follow-up reminders.

Instead of maintaining a real-time network connection, these two agents communicate asynchronously using **Shared User-Persistent State (`VertexAiSessionService`)** via the Agent Development Kit (ADK).

---

## 📂 Repository Structure

```text
.
├── ARCHITECTURE.md      # Detailed production architecture & session state lifecycle
├── DESIGN_SPEC.md       # Core functional specifications, constraints, and success criteria
├── morning-agent/       # Morning Coffee (Plan Producer) Agent deployment package
├── afternoon-agent/     # Afternoon Tea (Reconciliation Consumer) Agent deployment package
└── ref-a2a/             # Reference A2A protocol interoperability package
```

---

## 🚀 Prerequisites & Setup

Ensure you have the following installed on your development machine:
* **[uv](https://docs.astral.sh/uv/)**: Fast Python package and environment manager (`uv add <package>`).
* **[Google Cloud SDK](https://cloud.google.com/sdk/docs/install)**: Configured with active credentials (`gcloud auth login`).
* **GNU Make**: For running lifecycle automation commands.

### Authenticate with Google Cloud
```bash
gcloud config set project <YOUR_GCP_PROJECT_ID>
gcloud auth application-default login
```

---

## 💻 Local Development & Playground

Each agent is packaged independently using ADK. You can launch a local interactive development playground for real-time iteration.

### Launching Morning Coffee Agent locally:
```bash
cd morning-agent
make install
make playground
```

### Launching Afternoon Tea Agent locally:
```bash
cd afternoon-agent
make install
make playground
```

> **Tip**: The local playground automatically reloads whenever you modify the core agent logic located in `app/agent.py`.

---

## 🔗 Decoupled State Handoff Protocol

State persistence between the Morning and Afternoon agents relies on the `"user:"` session state prefix pattern in ADK.

1. **Morning Plan Storage**:
   ```python
   # Inside morning-agent/app/agent.py
   tool_context.state["user:morning_plan"] = daily_prep_details
   ```
2. **Afternoon Baseline Retrieval**:
   ```python
   # Inside afternoon-agent/app/agent.py
   session = await session_service.get_session(
       app_name="morning-agent",
       user_id=tool_context.session.user_id,
       session_id=session_key
   )
   ```

For deep-dive technical diagrams, refer to [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 🧪 Testing & Interoperability

### Run Unit and Integration Tests
```bash
# Run tests for Morning Agent
cd morning-agent && make test

# Run tests for Afternoon Agent
cd afternoon-agent && make test
```

### Launch A2A Protocol Inspector
To inspect Agent-to-Agent protocol payloads and simulate inter-agent communication:
```bash
make inspector
```

### Run Evaluation Suite (LLM-as-Judge)
Evaluate response accuracy, deduplication rates, and safety compliance against standard evalsets:
```bash
make eval EVALSET=tests/eval/evalsets/workday.evalset.json
```

---

## ☁️ Production Deployment

Deploy the agents directly as containerized Vertex AI Agent Engine endpoints:

```bash
# Deploy Morning Coffee Agent
cd morning-agent && make deploy

# Deploy Afternoon Tea Agent
cd afternoon-agent && make deploy
```

### Project Automation
* **Add CI/CD pipelines & Terraform**: `uvx agent-starter-pack enhance`
* **One-command full CI/CD deployment**: `uvx agent-starter-pack setup-cicd`

---

## 📊 Observability

Deployed agents automatically export structured telemetry to:
* **Google Cloud Trace**: Full agent reasoning and execution spans.
* **BigQuery Agent Analytics**: Prompt/response logging and tool execution metrics.
* **Cloud Logging**: System and execution logs.
