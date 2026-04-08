# 🚀 Support Ticket Triage AI Environment

A high-performance simulation environment for evaluating AI agents in customer support workflows, strictly adhering to the **OpenEnv 0.2.0** specification for the Meta x Scaler Hackathon.

## 📌 Project Overview
This project simulates a real-world help desk system. It provides a playground where AI agents interact with support tickets to perform classification, prioritization, and resolution. The environment uses **FastAPI** to provide a RESTful interface for agents to reset state and execute actions.

### Key Features
- **Strict Range Scoring:** Rewards are mathematically clamped between $0.01$ and $0.99$ to meet validator constraints.
- **SLA-Driven Logic:** Advanced reward weighting for "Enterprise" vs "Free" customer tiers.
- **Proxy-Ready:** Fully compatible with LiteLLM proxies for transparent inference tracking.
- **Fail-Fast Architecture:** Robust error handling ensures the `[END]` signal is always emitted.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10
- **Framework:** FastAPI
- **Validation:** Pydantic v2
- **LLM Integration:** OpenAI SDK (v1.0+)
- **Specification:** OpenEnv 0.2.0

---

## 📂 Project Structure
- **`server/app.py`**: The core environment logic and multi-mode entry point.
- **`server/models.py`**: Pydantic schemas for strict data enforcement.
- **`inference.py`**: Mandatory baseline script using the Scaler LLM Proxy.
- **`pyproject.toml`**: Project metadata and `server` script mapping.

---

## 📊 Evaluation Tasks & Rewards
To satisfy the "Dynamic Grader" requirement, scores are calculated based on agent precision:

| Task ID | Difficulty | Logic | Max Score |
| :--- | :--- | :--- | :--- |
| `triage_basics_v1` | Easy | Category Classification | `0.50` |
| `vip_priority_v1` | Medium | Enterprise Escalation (SLA) | `0.75` |
| `full_resolve_v1` | Hard | Full Lifecycle Resolution | `0.99` |

*Note: All "Perfect" scores are capped at 0.99 and "Failures" start at 0.01 to remain within the strictly $(0, 1)$ range.*

---

## 🚀 Getting Started

### 1. Start the Environment
The server is mapped as a global command via `pyproject.toml`.

###Set your environment variables and run the validator-ready script:

export API_BASE_URL="[https://router.huggingface.co/v1](https://router.huggingface.co/v1)"
export API_KEY="your_hf_token"
python inference.py

### 3.Standardized Benchmark Output

[START] task=full_resolve_v1 env=support-triage model=gpt-4o
[STEP] step=1 action=classify(T1) reward=0.20 done=false error=null
[STEP] step=2 action=prioritize(T1) reward=0.30 done=false error=null
[STEP] step=3 action=resolve(T1) reward=0.49 done=true error=null
[END] success=true steps=3 score=0.99 rewards=0.20,0.30,0.49
```bash
pip install -e .
server
