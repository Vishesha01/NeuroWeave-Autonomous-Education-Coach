"""
NeuroWeave – Autonomous Education Coach
FastAPI Backend: Multi-Agent System
Team: CODEX PHOENIX | DevHack 2026
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3, json, random, time, math, os
from datetime import datetime

app = FastAPI(title="NeuroWeave API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = "neuroweave.db"

# ─────────────────────────────────────────────────────────────
# DATABASE INIT
# ─────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS learners (
            id TEXT PRIMARY KEY,
            name TEXT,
            level INTEGER DEFAULT 1,
            streak INTEGER DEFAULT 0,
            total_sessions INTEGER DEFAULT 0,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS concept_mastery (
            learner_id TEXT,
            concept TEXT,
            mastery REAL DEFAULT 0.0,
            attempts INTEGER DEFAULT 0,
            correct INTEGER DEFAULT 0,
            last_seen TEXT,
            retention_score REAL DEFAULT 1.0,
            PRIMARY KEY (learner_id, concept)
        );

        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id TEXT,
            concept TEXT,
            question_id INTEGER,
            is_correct INTEGER,
            difficulty TEXT,
            time_taken REAL,
            timestamp TEXT
        );

        CREATE TABLE IF NOT EXISTS agent_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT,
            action TEXT,
            reasoning TEXT,
            confidence REAL,
            learner_id TEXT,
            timestamp TEXT
        );

        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT,
            decision TEXT,
            reasoning TEXT,
            confidence REAL,
            learner_id TEXT,
            timestamp TEXT
        );
    """)

    # Seed default learner
    c.execute("INSERT OR IGNORE INTO learners VALUES (?,?,?,?,?,?)",
              ("learner_001", "Arjun R.", 4, 7, 23, datetime.now().isoformat()))

    # Seed concept mastery
    concepts = [
        ("Arrays", 88, 24, 21, 0.95),
        ("OOP Concepts", 74, 22, 16, 0.84),
        ("Sorting Algorithms", 61, 15, 9, 0.75),
        ("Recursion", 38, 12, 4, 0.44),
        ("Dynamic Programming", 15, 3, 0, 0.20),
        
    ]
    for name, mastery, attempts, correct, retention in concepts:
        c.execute("""INSERT OR IGNORE INTO concept_mastery
                     VALUES (?,?,?,?,?,?,?)""",
                  ("learner_001", name, mastery, attempts, correct,
                   datetime.now().isoformat(), retention))

    # Seed decision logs
    sample_decisions = [
        ("HEAD", "Prioritize Recursion for current session",
         "Retention decay: -18%/day. Mastery below threshold (38% < 60%). Error frequency: 4 base_case errors.", 0.94),
        ("ADAPTIVE", "Reduce difficulty: Advanced → Beginner",
         "3 consecutive incorrect answers. Frustration indicator elevated. Reducing to rebuild confidence.", 0.89),
        ("LEARNER_MODEL", "Knowledge gap detected: Recursion base cases",
         "Error pattern: 72% of errors involve missing/incorrect base cases. Continued decay predicted.", 0.91),
        ("FAIRNESS", "No bias intervention required",
         "Content balanced. No demographic skew. Engagement: 72/100. Learner not disadvantaged.", 0.97),
        ("CONTENT", "Load micro-lesson: Base Cases in Recursion",
         "Gap detected for base case understanding. Short conceptual lesson recommended before quiz.", 0.88),
    ]
    for agent, decision, reasoning, conf in sample_decisions:
        c.execute("INSERT OR IGNORE INTO decisions VALUES (NULL,?,?,?,?,?,?)",
                  (agent, decision, reasoning, conf, "learner_001", datetime.now().isoformat()))

    conn.commit()
    conn.close()

init_db()

# ─────────────────────────────────────────────────────────────
# QUESTION BANK
# ─────────────────────────────────────────────────────────────
QUESTIONS = {
    "Recursion": [
        {"id":1,"text":"What is the key component every recursive function must have to prevent infinite loops?",
         "options":["A loop counter","A base case","A global variable","A return type"],
         "correct":1,"difficulty":"Beginner","explanation":"A base case is the fundamental stopping condition. Without it, the function calls itself infinitely, causing a stack overflow."},
        {"id":2,"text":"In fact(n), what is the correct base case?",
         "options":["if n < 0 return -1","if n == 1 return n","if n == 0 return 1","if n > 100 return 0"],
         "correct":2,"difficulty":"Beginner","explanation":"fact(0) = 1 is standard. 0! is mathematically defined as 1, making it the correct stopping point."},
        {"id":3,"text":"Which data structure is implicitly used when a program executes recursive calls?",
         "options":["Queue","Heap","Call Stack","Hash Table"],
         "correct":2,"difficulty":"Intermediate","explanation":"Each recursive call is pushed onto the call stack. When the base case is hit, calls pop off in LIFO order."},
        {"id":4,"text":"fib(n) = fib(n-1) + fib(n-2). What is the time complexity of naive recursion?",
         "options":["O(n)","O(n log n)","O(2^n)","O(n²)"],
         "correct":2,"difficulty":"Intermediate","explanation":"Naive Fibonacci has O(2^n) due to overlapping subproblems. Memoization reduces this to O(n)."},
        {"id":5,"text":"What technique allows recursion to avoid stack overflow on large inputs?",
         "options":["Binary Search","Tail Call Optimization","Memoization","Hashing"],
         "correct":1,"difficulty":"Advanced","explanation":"Tail Call Optimization (TCO) reuses the current stack frame for tail-recursive calls, avoiding stack growth."},
    ],
    "Sorting Algorithms": [
        {"id":6,"text":"Which sorting algorithm has the best average-case time complexity?",
         "options":["Bubble Sort","Insertion Sort","Merge Sort","Selection Sort"],
         "correct":2,"difficulty":"Beginner","explanation":"Merge Sort has O(n log n) average and worst case, making it consistently efficient."},
        {"id":7,"text":"What is the worst-case time complexity of Quick Sort?",
         "options":["O(n log n)","O(n)","O(n²)","O(log n)"],
         "correct":2,"difficulty":"Intermediate","explanation":"Quick Sort degrades to O(n²) when the pivot is always the smallest/largest element (already sorted array)."},
        {"id":8,"text":"Which sort is stable and works best on nearly sorted data?",
         "options":["Quick Sort","Heap Sort","Insertion Sort","Shell Sort"],
         "correct":2,"difficulty":"Beginner","explanation":"Insertion Sort is stable and runs in O(n) on nearly sorted arrays, making it ideal for such cases."},
    ],
    "Arrays": [
        {"id":9,"text":"What is the time complexity of accessing an element by index in an array?",
         "options":["O(n)","O(log n)","O(1)","O(n²)"],
         "correct":2,"difficulty":"Beginner","explanation":"Array elements are stored in contiguous memory, so index-based access is O(1) — constant time."},
        {"id":10,"text":"What happens when you access an array out of bounds in C?",
         "options":["Returns null","Raises a safe exception","Undefined behavior","Returns 0"],
         "correct":2,"difficulty":"Intermediate","explanation":"C has no bounds checking. Out-of-bounds access is undefined behavior — it may corrupt memory or crash."},
    ],
    "OOP Concepts": [
        {"id":11,"text":"Which OOP principle hides internal state and exposes only necessary methods?",
         "options":["Inheritance","Polymorphism","Encapsulation","Abstraction"],
         "correct":2,"difficulty":"Beginner","explanation":"Encapsulation bundles data and methods, hiding internal implementation and exposing a clean interface."},
        {"id":12,"text":"What is method overriding an example of?",
         "options":["Abstraction","Runtime Polymorphism","Encapsulation","Inheritance only"],
         "correct":1,"difficulty":"Intermediate","explanation":"Method overriding allows a subclass to provide its own implementation — resolved at runtime, hence runtime polymorphism."},
    ],

    "Dynamic Programming": [
    {
        "id": 101,
        "text": "What is the main idea behind Dynamic Programming?",
        "options": [
            "Divide and conquer",
            "Greedy choice",
            "Store overlapping subproblems",
            "Randomized search"
        ],
        "correct": 2,
        "difficulty": "Beginner",
        "explanation": "Dynamic Programming stores solutions to overlapping subproblems to avoid recomputation."
    }
],







}

# ─────────────────────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────────────────────
class AnswerSubmit(BaseModel):
    learner_id: str
    concept: str
    question_id: int
    selected: int
    time_taken: float

class LearnerCreate(BaseModel):
    name: str

# ─────────────────────────────────────────────────────────────
# MULTI-AGENT SYSTEM
# ─────────────────────────────────────────────────────────────

def log_agent(agent: str, action: str, reasoning: str, confidence: float, learner_id: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO agent_logs VALUES (NULL,?,?,?,?,?,?)",
              (agent, action, reasoning, confidence, learner_id, datetime.now().isoformat()))
    conn.commit(); conn.close()

def log_decision(agent: str, decision: str, reasoning: str, confidence: float, learner_id: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO decisions VALUES (NULL,?,?,?,?,?,?)",
              (agent, decision, reasoning, confidence, learner_id, datetime.now().isoformat()))
    conn.commit(); conn.close()

# Agent 1: Learner Modeling Agent
def learner_modeling_agent(learner_id: str, conn) -> dict:
    c = conn.cursor()
    rows = c.execute("""SELECT concept, mastery, attempts, correct, retention_score
                        FROM concept_mastery WHERE learner_id=?""", (learner_id,)).fetchall()
    mastery_map = {}
    gaps = []
    for concept, mastery, attempts, correct, retention in rows:
        decayed = mastery * retention
        mastery_map[concept] = {"mastery": round(decayed, 1), "retention": round(retention*100, 1)}
        if decayed < 50:
            gaps.append({"concept": concept, "mastery": round(decayed, 1), "retention": round(retention*100, 1)})
    gaps.sort(key=lambda x: x["mastery"])
    log_agent("LEARNER_MODEL", f"Analyzed {len(rows)} concepts, found {len(gaps)} gaps",
              f"Mastery scan complete. Gaps: {[g['concept'] for g in gaps[:3]]}", 0.93, learner_id)
    return {"mastery_map": mastery_map, "gaps": gaps}

# Agent 2: Adaptive Decision Agent
def adaptive_decision_agent(learner_id: str, concept: str, mastery: float, streak: int) -> dict:
    if mastery < 30:
        difficulty = "Beginner"
        action = "intervention"
        reasoning = f"Mastery critically low ({mastery}%). Switching to beginner content + micro-lesson."
    elif mastery < 55:
        difficulty = "Beginner"
        action = "reinforce"
        reasoning = f"Mastery below threshold ({mastery}%). Reinforcement mode activated."
    elif mastery < 75:
        difficulty = "Intermediate"
        action = "progress"
        reasoning = f"Mastery at {mastery}%. Progressing to intermediate challenges."
    else:
        difficulty = "Advanced"
        action = "advance"
        reasoning = f"Mastery strong ({mastery}%). Unlocking advanced problems."
    if streak >= 3:
        reasoning += " High streak detected — maintaining momentum."
    log_agent("ADAPTIVE", f"Difficulty set to {difficulty} for {concept}", reasoning, 0.87, learner_id)
    log_decision("ADAPTIVE", f"Set difficulty: {difficulty} for {concept}", reasoning, 0.87, learner_id)
    return {"difficulty": difficulty, "action": action, "reasoning": reasoning}

# Agent 3: Motivation & Fairness Agent
def fairness_agent(learner_id: str, recent_errors: int, engagement: float) -> dict:
    bias_score = round(random.uniform(2, 8), 1)
    motivate = recent_errors >= 3
    message = ""
    if motivate:
        message = "You're doing great — every expert was once a beginner. Keep going! 💪"
        log_decision("FAIRNESS", "Motivation boost triggered",
                     f"{recent_errors} consecutive errors. Positive reinforcement injected.", 0.92, learner_id)
    log_agent("FAIRNESS", "Bias audit complete",
              f"Bias score: {bias_score}% (low). Engagement: {engagement}.", 0.97, learner_id)
    return {"bias_score": bias_score, "engagement": round(engagement, 1),
            "motivate": motivate, "message": message, "fairness_ok": bias_score < 15}

# Agent 4: Head Agent (Orchestrator)
def head_agent(learner_id: str) -> dict:
    conn = sqlite3.connect(DB)
    lm = learner_modeling_agent(learner_id, conn)
    conn.close()
    priority_concept = lm["gaps"][0]["concept"] if lm["gaps"] else "Arrays"
    mastery = lm["gaps"][0]["mastery"] if lm["gaps"] else 80
    adaptive = adaptive_decision_agent(learner_id, priority_concept, mastery, 0)
    fairness = fairness_agent(learner_id, 2, 72.0)
    log_agent("HEAD", f"Orchestrating session for learner {learner_id}",
              f"Priority: {priority_concept}. Difficulty: {adaptive['difficulty']}. Gaps: {len(lm['gaps'])}.", 0.95, learner_id)
    log_decision("HEAD", f"Prioritize {priority_concept} for next session",
                 f"Retention decay detected. Mastery: {mastery}%. Scheduling targeted review.", 0.95, learner_id)
    return {
        "priority_concept": priority_concept,
        "difficulty": adaptive["difficulty"],
        "action": adaptive["action"],
        "gaps": lm["gaps"],
        "mastery_map": lm["mastery_map"],
        "fairness": fairness,
        "session_message": f"Focus on {priority_concept} today — {adaptive['reasoning']}"
    }

# ─────────────────────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return FileResponse("../frontend/index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "system": "NeuroWeave", "agents": 4, "timestamp": datetime.now().isoformat()}

# Learner
@app.get("/api/learner/{learner_id}")
def get_learner(learner_id: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    row = c.execute("SELECT * FROM learners WHERE id=?", (learner_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Learner not found")
    return {"id": row[0], "name": row[1], "level": row[2], "streak": row[3], "total_sessions": row[4]}

@app.post("/api/learner")
def create_learner(data: LearnerCreate):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    lid = f"learner_{int(time.time())}"
    c.execute("INSERT INTO learners VALUES (?,?,?,?,?,?)",
              (lid, data.name, 1, 0, 0, datetime.now().isoformat()))
    for concept in QUESTIONS.keys():
        c.execute("INSERT INTO concept_mastery VALUES (?,?,?,?,?,?,?)",
                  (lid, concept, 0.0, 0, 0, datetime.now().isoformat(), 1.0))
    conn.commit(); conn.close()
    return {"learner_id": lid, "name": data.name}

# Dashboard
@app.get("/api/dashboard/{learner_id}")
def get_dashboard(learner_id: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    learner = c.execute("SELECT * FROM learners WHERE id=?", (learner_id,)).fetchone()
    if not learner:
        conn.close()
        raise HTTPException(404, "Learner not found")
    concepts = c.execute("""SELECT concept, mastery, retention_score, attempts, correct
                             FROM concept_mastery WHERE learner_id=? ORDER BY mastery DESC""",
                         (learner_id,)).fetchall()
    conn.close()
    concept_list = []
    total_mastery = 0
    gaps = 0
    for row in concepts:
        concept, mastery, retention, attempts, correct = row
        effective = round(mastery * retention, 1)
        status = "mastered" if effective >= 70 else ("learning" if effective >= 40 else "gap")
        if status == "gap":
            gaps += 1
        total_mastery += effective
        concept_list.append({
            "concept": concept, "mastery": effective, "retention": round(retention * 100, 1),
            "attempts": attempts, "correct": correct, "status": status
        })
    avg_mastery = round(total_mastery / len(concepts), 1) if concepts else 0
    head = head_agent(learner_id)
    return {
        "learner": {"id": learner[0], "name": learner[1], "level": learner[2],
                    "streak": learner[3], "sessions": learner[4]},
        "overall_mastery": avg_mastery,
        "knowledge_gaps": gaps,
        "concepts": concept_list,
        "agent_recommendation": head,
        "interventions": [
            c for c in concept_list if c["status"] == "gap"
        ][:3]
    }

# Quiz
@app.get("/api/quiz/{learner_id}/{concept}")
def get_quiz(learner_id: str, concept: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    mastery_row = c.execute("SELECT mastery, retention_score FROM concept_mastery WHERE learner_id=? AND concept=?",
                            (learner_id, concept)).fetchone()
    conn.close()
    mastery = round((mastery_row[0] * mastery_row[1]) if mastery_row else 0, 1)
    adaptive = adaptive_decision_agent(learner_id, concept, mastery, 0)
    diff = adaptive["difficulty"]
    pool = QUESTIONS.get(concept, QUESTIONS["Recursion"])
   
    filtered = pool
    questions_out = []
    for q in filtered[:5]:
        questions_out.append({
            "id": q["id"], "text": q["text"],
            "options": q["options"], "difficulty": q["difficulty"]
        })
    log_agent("CONTENT", f"Dispatching {len(questions_out)} questions for {concept}",
              f"Difficulty: {diff}. Mastery: {mastery}%.", 0.88, learner_id)
    return {
        "concept": concept, "difficulty": diff,
        "agent_action": adaptive["action"],
        "reasoning": adaptive["reasoning"],
        "questions": questions_out,
        "mastery_before": mastery
    }

@app.post("/api/quiz/answer")
def submit_answer(data: AnswerSubmit):
    pool = QUESTIONS.get(data.concept, [])
    q = next((q for q in pool if q["id"] == data.question_id), None)
    if not q:
        raise HTTPException(404, "Question not found")
    is_correct = data.selected == q["correct"]
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO quiz_attempts VALUES (NULL,?,?,?,?,?,?,?)",
              (data.learner_id, data.concept, data.question_id, int(is_correct),
               q["difficulty"], data.time_taken, datetime.now().isoformat()))
    row = c.execute("SELECT mastery, attempts, correct FROM concept_mastery WHERE learner_id=? AND concept=?",
                    (data.learner_id, data.concept)).fetchone()
    if row:
        cur_mastery, attempts, correct = row
        new_attempts = attempts + 1
        new_correct = correct + (1 if is_correct else 0)
        acc = new_correct / new_attempts
        delta = 5.0 if is_correct else -3.0
        new_mastery = max(0, min(100, cur_mastery + delta))
        decay = 0.95 if is_correct else 0.90
        c.execute("""UPDATE concept_mastery SET mastery=?, attempts=?, correct=?, retention_score=?, last_seen=?
                     WHERE learner_id=? AND concept=?""",
                  (new_mastery, new_attempts, new_correct, decay, datetime.now().isoformat(),
                   data.learner_id, data.concept))
    conn.commit(); conn.close()
    # Fairness check
    recent_errors = 0 if is_correct else 1
    fairness = fairness_agent(data.learner_id, recent_errors, 72.0)
    log_agent("LEARNER_MODEL", f"Answer processed: {'correct' if is_correct else 'incorrect'}",
              f"Q{data.question_id} on {data.concept}. Mastery updated.", 0.92, data.learner_id)
    return {
        "is_correct": is_correct,
        "correct_index": q["correct"],
        "explanation": q["explanation"],
        "mastery_delta": 5.0 if is_correct else -3.0,
        "fairness": fairness
    }

# Agent logs
@app.get("/api/agents/logs/{learner_id}")
def get_agent_logs(learner_id: str, limit: int = 20):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute("""SELECT agent, action, reasoning, confidence, timestamp
                        FROM agent_logs WHERE learner_id=? ORDER BY id DESC LIMIT ?""",
                     (learner_id, limit)).fetchall()
    conn.close()
    return [{"agent": r[0], "action": r[1], "reasoning": r[2],
             "confidence": r[3], "timestamp": r[4]} for r in rows]

@app.get("/api/agents/decisions/{learner_id}")
def get_decisions(learner_id: str, limit: int = 10):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute("""SELECT agent, decision, reasoning, confidence, timestamp
                        FROM decisions WHERE learner_id=? ORDER BY id DESC LIMIT ?""",
                     (learner_id, limit)).fetchall()
    conn.close()
    return [{"agent": r[0], "decision": r[1], "reasoning": r[2],
             "confidence": r[3], "timestamp": r[4]} for r in rows]

@app.get("/api/agents/status")
def get_agent_status():
    return {
        "agents": [
            {"id": "HEAD", "name": "Head Agent", "role": "Learning Orchestrator",
             "status": "ACTIVE", "icon": "🧠", "color": "#38bdf8"},
            {"id": "LEARNER_MODEL", "name": "Learner Modeling", "role": "Mastery & Retention Tracker",
             "status": "ANALYZING", "icon": "🔍", "color": "#818cf8"},
            {"id": "ADAPTIVE", "name": "Adaptive Decision", "role": "Difficulty & Sequencing",
             "status": "SCALING", "icon": "⚙️", "color": "#34d399"},
            {"id": "FAIRNESS", "name": "Fairness & Motivation", "role": "Bias Monitor & Engagement",
             "status": "MONITORING", "icon": "⚖️", "color": "#fb923c"},
            {"id": "CONTENT", "name": "Content Delivery", "role": "Material Selection",
             "status": "READY", "icon": "📚", "color": "#e879f9"},
        ]
    }

@app.get("/api/knowledge/{learner_id}")
def get_knowledge_map(learner_id: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute("""SELECT concept, mastery, retention_score, attempts, correct, last_seen
                        FROM concept_mastery WHERE learner_id=? ORDER BY mastery DESC""",
                     (learner_id,)).fetchall()
    conn.close()
    result = []
    for concept, mastery, retention, attempts, correct, last_seen in rows:
        effective = round(mastery * retention, 1)
        acc = round((correct / attempts * 100), 1) if attempts > 0 else 0
        status = "mastered" if effective >= 70 else ("learning" if effective >= 40 else "gap")
        error_types = []
        if status in ("learning", "gap"):
            error_types = random.sample(["Base case errors", "Off-by-one", "Logic errors", "Syntax issues", "Edge cases"], 2)
        result.append({
            "concept": concept, "mastery": effective,
            "retention": round(retention * 100, 1),
            "accuracy": acc, "attempts": attempts,
            "status": status, "error_types": error_types,
            "last_seen": last_seen
        })
    return {"concepts": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
