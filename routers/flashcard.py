"""Router for flashcard generation."""

import json
import re

from fastapi import APIRouter, HTTPException
from langchain_groq import ChatGroq
from pydantic import BaseModel

from config import settings

router = APIRouter(prefix="/flashcard", tags=["Flashcard"])

llm = ChatGroq(model="llama3-8b-8192", api_key=settings.groq_api_key, temperature=0.5)


class FlashcardRequest(BaseModel):
    content: str
    chapter: str
    subject: str
    grade: int


def _extract_json(text: str) -> dict:
    """Extract first valid JSON object from LLM response."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise ValueError(f"No valid JSON found: {text[:200]}")


@router.post("/generate")
def generate_flashcards(req: FlashcardRequest) -> dict:
    """Generate 8 Q&A flashcard pairs from chapter content."""
    prompt = f"""Generate exactly 8 flashcard question-answer pairs for {req.subject} Grade {req.grade}, chapter "{req.chapter}".

Content:
{req.content[:2500]}

Respond ONLY with JSON, no other text:
{{"flashcards":[{{"question":"What is ...?","answer":"It is ..."}}]}}"""
    try:
        response = llm.invoke(prompt)
        data = _extract_json(response.content)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {e}")
