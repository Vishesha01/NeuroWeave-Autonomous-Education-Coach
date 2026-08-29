# NeuroWeave — Autonomous Education Coach

> A cognitive-aware multi-agent system that models learner cognition, identifies knowledge gaps, and dynamically adapts learning paths based on learner performance and progress.

---

## Overview

NeuroWeave is an autonomous education coaching system designed to provide personalized and adaptive learning experiences.

The system analyzes learner mastery, retention patterns, error patterns, and engagement to dynamically adapt learning paths. A multi-agent architecture coordinates learner modeling, adaptive decision-making, fairness monitoring, motivation, and content delivery.

The platform also provides explainable decision logs, enabling learning decisions to be tracked with their reasoning and confidence information.

---

## Key Features

- **Adaptive Learning** — Dynamically adjusts learning difficulty based on learner performance and mastery.
- **Knowledge Gap Detection** — Identifies concepts requiring additional attention using mastery and retention patterns.
- **Learner Modeling** — Tracks concept mastery, retention decay, and error patterns.
- **Personalized Learning Paths** — Re-sequences concepts and recommends appropriate learning interventions.
- **Adaptive Quiz Engine** — Adjusts quiz difficulty according to the learner's current mastery level.
- **Explainable AI** — Records agent decisions with reasoning and confidence information.
- **Fairness Monitoring** — Tracks fairness-related metrics during learning sessions.
- **Agent Monitoring** — Provides agent status, action logs, and decision logs.
- **Persistent Learner Data** — Maintains learner state using SQLite.
- **RESTful API** — Provides backend endpoints for learner management, quizzes, knowledge maps, and agent monitoring.

---

## System Architecture

NeuroWeave uses a multi-agent architecture in which a central **Head Agent** coordinates specialized agents.

```text
                         ┌─────────────────────────┐
                         │       HEAD AGENT        │
                         │   Learning Orchestrator │
                         └────────────┬────────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             ▼                        ▼                        ▼
    ┌──────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
    │ Learner Modeling │    │ Adaptive Decision│    │ Fairness & Motivation│
    │      Agent       │    │      Agent       │    │        Agent         │
    └──────────────────┘    └──────────────────┘    └─────────────────────┘
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Content Delivery Agent  │
                         │ Questions & Materials   │
                         └─────────────────────────┘
```

### Agent Responsibilities

| Agent | Responsibility |
|---|---|
| **Head Agent** | Orchestrates the learning workflow, delegates tasks, and manages sessions |
| **Learner Modeling Agent** | Tracks mastery, retention decay, and learner error patterns |
| **Adaptive Decision Agent** | Adjusts difficulty, re-sequences concepts, and determines interventions |
| **Fairness & Motivation Agent** | Monitors fairness, engagement, and explainability-related information |
| **Content Delivery Agent** | Selects appropriate questions and learning materials |

---

## Project Structure

```text
NeuroWeave-Autonomous-Education-Coach/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   └── index.html
│
└── README.md
```

---

## Technology Stack

| Component | Technology |
|---|---|
| **Backend** | Python, FastAPI |
| **Frontend** | HTML, CSS, JavaScript |
| **Database** | SQLite |
| **Learning Logic** | Rule Engine, Lightweight ML Heuristics |
| **Agent Architecture** | Custom Python Multi-Agent Orchestrator |
| **API** | RESTful API |

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Check system health |
| `GET` | `/api/learner/{id}` | Retrieve learner profile |
| `POST` | `/api/learner` | Create a learner |
| `GET` | `/api/dashboard/{id}` | Retrieve dashboard data and trigger orchestration |
| `GET` | `/api/quiz/{id}/{concept}` | Retrieve adaptive quiz questions |
| `POST` | `/api/quiz/answer` | Submit an answer and update mastery |
| `GET` | `/api/knowledge/{id}` | Retrieve the learner knowledge map |
| `GET` | `/api/agents/status` | Retrieve agent status |
| `GET` | `/api/agents/logs/{id}` | Retrieve agent action logs |
| `GET` | `/api/agents/decisions/{id}` | Retrieve explainable AI decision logs |

---

## Getting Started

### Prerequisites

Before running the project, make sure you have:

- Python 3.x
- pip
- A modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/Vishesha01/NeuroWeave-Autonomous-Education-Coach.git
cd NeuroWeave-Autonomous-Education-Coach
```

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

### 3. Access API Documentation

FastAPI provides interactive API documentation at:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

The frontend is implemented using HTML, CSS, and JavaScript and does not require a build process.

From the project root, open:

```text
frontend/index.html
```

directly in a web browser.

Alternatively, start a local web server:

```bash
cd frontend
python -m http.server 3000
```

Then open:

```text
http://localhost:3000
```

---

## Learning Workflow

The system follows an adaptive learning workflow:

```text
Learner
   │
   ▼
Learning Request
   │
   ▼
Head Agent
   │
   ├──► Learner Modeling Agent
   │       └── Mastery + Retention + Error Patterns
   │
   ├──► Adaptive Decision Agent
   │       └── Difficulty + Concept Sequence + Interventions
   │
   ├──► Fairness & Motivation Agent
   │       └── Fairness + Engagement
   │
   └──► Content Delivery Agent
           └── Questions + Learning Materials
                    │
                    ▼
           Personalized Learning
                    │
                    ▼
             Decision Logging
```

---

## Explainable AI

NeuroWeave provides transparency into autonomous learning decisions through structured decision logs.

Decision information includes:

- Responsible agent
- Action performed
- Decision reasoning
- Confidence information
- Relevant learner context

These logs help developers and users understand the reasoning behind adaptive learning decisions.

---

## Knowledge Gap Detection

The system maintains learner knowledge information across different concepts.

Knowledge-gap detection uses learner performance and retention patterns to identify concepts that may require additional practice or intervention.

This information is used by the adaptive decision process to determine appropriate learning actions.

---

## Adaptive Quiz Engine

The adaptive quiz engine selects questions based on the learner's current mastery level.

The system can:

1. Evaluate the learner's current performance.
2. Update concept mastery after an answer.
3. Identify areas that require additional practice.
4. Adjust future question difficulty.
5. Support personalized learning progression.

---

## Demo Learner

A pre-seeded learner is available for demonstration and testing.

| Field | Value |
|---|---|
| **Learner** | Arjun R. |
| **Learner ID** | `learner_001` |
| **Concepts** | 12 |

The demo learner contains concepts with different mastery levels for demonstrating adaptive learning and knowledge-gap detection.

---

## Project Highlights

- Multi-agent system architecture
- Personalized and adaptive learning
- Learner knowledge modeling
- Knowledge-gap detection
- Adaptive quiz generation
- Explainable AI decision tracking
- Fairness monitoring
- RESTful API development
- Persistent learner data management
- Lightweight machine learning heuristics

---

## Future Enhancements

Potential improvements include:

- Integration with larger language models
- Advanced learner behavior prediction
- More sophisticated knowledge tracing
- Additional learning content formats
- Enhanced analytics and visualization
- User authentication and role-based access
- Cloud deployment and scalable storage

---

## License

This project is intended for educational and development purposes.
