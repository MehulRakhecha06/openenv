# 🚀 Support Ticket Triage AI Environment

A high-performance simulation environment for training and evaluating AI agents in customer support workflows. Built using the **OpenEnv** specification.

## 📌 Project Overview
This project simulates a real-world help desk system. It provides a playground where AI agents can interact with support tickets to perform classification, prioritization, and resolution. The environment uses **FastAPI** to provide a RESTful interface for agents to reset their state and take actions.

### Key Features
* **Automated Scoring:** Real-time reward calculation based on business logic.
* **Multi-Tier Logic:** Special handling for "Enterprise" vs "Basic" customers.
* **OpenEnv Compliant:** Ready for automated validation and benchmarking.
* **HITL Ready:** Designed for future Human-in-the-Loop integration.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **Framework:** FastAPI (High-performance API)
* **Data Validation:** Pydantic (Strict schema enforcement)
* **Deployment:** Docker (Hugging Face Spaces)
* **Agent Brain:** GPT-4o (via OpenAI SDK)

---

## 📂 Project Structure
* `app.py`: The core environment logic and API endpoints.
* `models.py`: Pydantic data models for Tickets, Observations, and Actions.
* `inference.py`: The AI agent script that performs the triage tasks.
* `openenv.yaml`: Metadata defining the tasks and difficulty levels.
* `Dockerfile`: Containerization setup for easy deployment.

---

## 📊 Environment Tasks

| Task ID | Difficulty | Requirements | Max Score |
| :--- | :--- | :--- | :--- |
| `triage_basics_v1` | **Easy** | Classify ticket category | 0.2 |
| `vip_priority_v1` | **Medium** | Escalate Enterprise customers | 0.5 |
| `full_resolve_v1` | **Hard** | Complete the full triage lifecycle | 1.0 |

---

## 🚀 Getting Started

### 1. Run the Environment (Local)
Ensure you have the dependencies installed:
```bash
pip install fastapi uvicorn pydantic requests
python app.py

# Windows (PowerShell)
$env:HF_TOKEN="your_openai_key"
python inference.py

## Benchmark results
[START] {"task_id": "full_resolve_v1", "model": "gpt-4o"}
[STEP] {"step": 0, "action": {"action_type": "classify"...}, "reward": 0.2}
[STEP] {"step": 1, "action": {"action_type": "prioritize"...}, "reward": 0.3}
[STEP] {"step": 2, "action": {"action_type": "resolve"...}, "reward": 0.5}
[END] {"final_score": 1.0}