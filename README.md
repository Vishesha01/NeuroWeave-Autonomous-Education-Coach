# ⬡ NeuroWeave – Autonomous Education Coach
### Team CODEX PHOENIX · DevHack 2026 · Problem: AIPSO5

> A cognitive-aware multi-agent system that models learner cognition, predicts knowledge gaps, and dynamically adapts learning paths.

---

## 🏗️ Architecture

```
neuroweave/
├── backend/
│   ├── main.py           ← FastAPI app + 4-agent system + SQLite DB
│   └── requirements.txt
└── frontend/
    └── index.html        ← Full dashboard UI (no build step needed)
```

### Multi-Agent Layers
| Agent | Role |
|---|---|
| 🧠 Head Agent | Learning Orchestrator — delegates tasks, manages session |
| 🔍 Learner Modeling Agent | Mastery tracking, retention decay, error patterns |
| ⚙️ Adaptive Decision Agent | Difficulty scaling, concept re-sequencing, interventions |
| ⚖️ Fairness & Motivation Agent | Bias monitoring, engagement, explainable decision logs |
| 📚 Content Delivery Agent | Question selection & material dispatch |

---

## 🚀 Quick Start

### 1. Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
API docs available at: http://localhost:8000/docs

### 2. Frontend
Open `frontend/index.html` directly in a browser.  
Or serve it:
```bash
cd frontend
python -m http.server 3000
# Open: http://localhost:3000
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | System health check |
| GET | `/api/learner/{id}` | Get learner profile |
| POST | `/api/learner` | Create new learner |
| GET | `/api/dashboard/{id}` | Full dashboard data (triggers Head Agent) |
| GET | `/api/quiz/{id}/{concept}` | Adaptive quiz questions |
| POST | `/api/quiz/answer` | Submit answer & update mastery |
| GET | `/api/knowledge/{id}` | Full knowledge map |
| GET | `/api/agents/status` | Live agent status |
| GET | `/api/agents/logs/{id}` | Agent action logs |
| GET | `/api/agents/decisions/{id}` | XAI decision logs |

---

## 🔑 Key Features

- **Adaptive Quiz Engine** — difficulty auto-adjusts per mastery level
- **Knowledge Gap Detection** — retention decay modeled per concept
- **Explainable AI** — every agent decision logged with reasoning + confidence
- **Fairness Monitor** — bias score tracked each session
- **SQLite persistence** — all learner state saved across sessions
- **CORS-enabled** — frontend + backend run independently

---

## 💻 Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python |
| Database | SQLite (persistent learner storage) |
| Frontend | Vanilla HTML/CSS/JS |
| Logic | Rule Engine + Lightweight ML heuristics |
| Agents | Custom Python multi-agent orchestrator |

---

## 🧪 Demo Learner
Pre-seeded: **Arjun R.** (`learner_001`) with 12 concepts across varying mastery levels.
