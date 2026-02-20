"""Router for quiz generation and result storage."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from langchain_groq import ChatGroq
from pydantic import BaseModel

from config import settings

router = APIRouter(prefix="/quiz", tags=["Quiz"])

RESULTS_FILE = Path(__file__).parent.parent / "quiz_results.json"

llm = ChatGroq(model="llama-3.1-8b-instant", api_key=settings.groq_api_key, temperature=0.4)


# ── Schemas ────────────────────────────────────────────────────────────────
class QuizGenRequest(BaseModel):
    content: str
    chapter: str
    subject: str
    grade: int


class QuizResult(BaseModel):
    student: str
    grade: int
    subject: str
    chapter: str
    score: int
    total: int = 5
    answers: List[str] = []


# ── Helpers ────────────────────────────────────────────────────────────────
def _load_results() -> list:
    if RESULTS_FILE.exists():
        return json.loads(RESULTS_FILE.read_text())
    return []


def _save_results(results: list) -> None:
    RESULTS_FILE.write_text(json.dumps(results, indent=2))


def _extract_json(text: str) -> dict:
    """Extract the first valid JSON object from an LLM response, handling all formats."""
    # Strip markdown code fences
    text = re.sub(r"```(?:json)?", "", text).strip()
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Find the outermost { ... } block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise ValueError(f"No valid JSON found in response: {text[:200]}")


# ── Endpoints ──────────────────────────────────────────────────────────────
@router.post("/generate")
def generate_quiz(req: QuizGenRequest) -> dict:
    """Generate 5 MCQ questions from chapter content using the LLM."""
    prompt = f"""You are a quiz generator. Generate exactly 5 multiple-choice questions for {req.subject} Grade {req.grade}, chapter "{req.chapter}".

Content:
{req.content[:2500]}

Respond ONLY with a JSON object in this exact format, no other text:
{{"questions":[{{"question":"...?","options":["A. ...","B. ...","C. ...","D. ..."],"answer":"A"}}]}}"""
    try:
        response = llm.invoke(prompt)
        data = _extract_json(response.content)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {e}")



@router.post("/submit")
def submit_result(result: QuizResult) -> dict:
    """Store a student's quiz result."""
    results = _load_results()
    entry = result.model_dump()
    entry["timestamp"] = datetime.now().isoformat()
    results.append(entry)
    _save_results(results)
    return {"status": "stored", "score": result.score, "total": result.total}


@router.get("/results")
def get_results(student: str | None = None) -> list:
    """Get all quiz results, optionally filtered by student name."""
    results = _load_results()
    if student:
        results = [r for r in results if r.get("student") == student]
    return results
