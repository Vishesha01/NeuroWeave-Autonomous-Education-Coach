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

---

## System Architecture

NeuroWeave follows a multi-agent architecture where a central **Head Agent** coordinates specialized agents responsible for learner analysis, adaptive decisions, fairness and motivation, and content delivery.

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
                         │  Content Delivery Agent│
                         │ Questions & Materials   │
                         └─────────────────────────┘
Agent Responsibilities
Agent	Responsibility
Head Agent	Orchestrates the learning workflow, delegates tasks, and manages sessions
Learner Modeling Agent	Tracks mastery, retention decay, and learner error patterns
Adaptive Decision Agent	Adjusts difficulty, re-sequences concepts, and determines interventions
Fairness & Motivation Agent	Monitors fairness, engagement, and explainability-related information
Content Delivery Agent	Selects appropriate questions and learning materials
Project Structure
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
Technology Stack
Component	Technology
Backend	Python, FastAPI
Frontend	HTML, CSS, JavaScript
Database	SQLite
Learning Logic	Rule Engine, Lightweight ML Heuristics
Agent Architecture	Custom Python Multi-Agent Orchestrator
API	RESTful API
API Reference
Method	Endpoint	Description
GET	/api/health	Check system health
GET	/api/learner/{id}	Retrieve learner profile
POST	/api/learner	Create a learner
GET	/api/dashboard/{id}	Retrieve dashboard data and trigger orchestration
GET	/api/quiz/{id}/{concept}	Retrieve adaptive quiz questions
POST	/api/quiz/answer	Submit an answer and update mastery
GET	/api/knowledge/{id}	Retrieve the learner knowledge map
GET	/api/agents/status	Retrieve agent status
GET	/api/agents/logs/{id}	Retrieve agent action logs
GET	/api/agents/decisions/{id}	Retrieve explainable AI decision logs
Getting Started
Prerequisites
Python 3.x
pip
Modern web browser
Backend Setup

Clone the repository:

git clone https://github.com/Vishesha01/NeuroWeave-Autonomous-Education-Coach.git
cd NeuroWeave-Autonomous-Education-Coach/backend

Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn main:app --reload --port 8000

The API will be available at:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs
Frontend Setup

The frontend does not require a build process.

Open:

frontend/index.html

directly in a browser.

Alternatively:

cd frontend
python -m http.server 3000

Then open:

http://localhost:3000
Learning Workflow
Learner
   │
   ▼
Learning Request
   │
   ▼
Head Agent
   │
   ├──► Learner Modeling
   │       └── Mastery + Retention + Error Patterns
   │
   ├──► Adaptive Decision
   │       └── Difficulty + Concept Sequence
   │
   ├──► Fairness & Motivation
   │       └── Fairness + Engagement
   │
   └──► Content Delivery
           └── Questions + Learning Materials
                    │
                    ▼
           Personalized Learning
                    │
                    ▼
             Decision Logging
Explainable AI

NeuroWeave provides transparency into autonomous learning decisions through structured decision logs.

Decision information includes:

Responsible agent
Action performed
Decision reasoning
Confidence information
Relevant learner context

This enables developers and users to understand the reasoning behind adaptive learning decisions.

Demo Learner

A pre-seeded learner is available for demonstration and testing.

Field	Value
Learner	Arjun R.
Learner ID	learner_001
Concepts	12

The demo learner contains concepts with different mastery levels for demonstrating adaptive learning and knowledge-gap detection.

Project Highlights
Multi-agent system architecture
Personalized and adaptive learning
Learner knowledge modeling
Knowledge-gap detection
Adaptive quiz generation
Explainable AI decision tracking
Fairness monitoring
RESTful API development
Persistent learner data management
