from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

class CreateSession(BaseModel):
    job_description: str
    role: str | None = None
    level: str = "junior"

class AnswerSubmission(BaseModel):
    session_id: int
    question_id: int
    answer_text: str

app = FastAPI(title="LangGraph Mock Interview System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LIVE: Dict[int, Dict[str, Any]] = {}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/sessions")
async def create_session(payload: CreateSession):
    state = {
        "job_description": payload.job_description,
        "role": payload.role,
        "level": payload.level,
        "asked": [],
        "answers": [],
        "max_questions": 6,
        "done": False,
        "last_answer_text": None,
    }

    try:
        from app.graph import compiled_graph
    except Exception as e:
        raise HTTPException(500, f"Graph import failed: {e}")

    try:
        result = compiled_graph.run(state)
    except TypeError:
        result = await compiled_graph.run(state)

    session_key = id(result)
    LIVE[session_key] = result

    return {
        "session_key": session_key,
        "current_question": result.get("current_question"),
    }

@app.post("/sessions/{session_key}/answer")
async def submit_answer(session_key: int, payload: AnswerSubmission):
    state = LIVE.get(session_key)
    if not state:
        raise HTTPException(404, "Session not found")

    state["last_answer_text"] = payload.answer_text

    try:
        from app.graph import compiled_graph
    except Exception as e:
        raise HTTPException(500, f"Graph import failed: {e}")

    try:
        result = compiled_graph.run(state)
    except TypeError:
        result = await compiled_graph.run(state)

    LIVE[session_key] = result

    return {
        "session_key": session_key,
        "next_question": result.get("current_question"),
        "done": result.get("done", False),
        "feedback": result.get("feedback"),
    }
