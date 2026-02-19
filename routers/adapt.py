"""Router for POST /adapt — adaptive content generation with disability profile routing."""

import asyncio
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from langchain_groq import ChatGroq

from config import settings
from rag.pedagogy_store import retrieve_pedagogy
from rag.prompts import (
    SIMPLIFIED_PROMPT,
    TTS_SCRIPT_PROMPT,
    VISUAL_DESCRIPTION_PROMPT,
)
from rag.retriever import retrieve_with_feedback
from schemas import AdaptRequest, AdaptResponse

router = APIRouter()

# Maps each disability profile to the chains that should be invoked.
# None (no profile provided) runs all three chains.
PROFILE_CHAINS: Dict[Optional[str], List[str]] = {
    "dyslexia": ["simplified"],
    "adhd": ["simplified"],
    "cognitive": ["simplified", "tts_script"],
    "visual_impairment": ["visual_description", "tts_script"],
    "hearing_impairment": ["simplified", "visual_description"],
    None: ["simplified", "visual_description", "tts_script"],
}

_CHAIN_PROMPTS = {
    "simplified": SIMPLIFIED_PROMPT,
    "visual_description": VISUAL_DESCRIPTION_PROMPT,
    "tts_script": TTS_SCRIPT_PROMPT,
}


def _get_llm() -> ChatGroq:
    """Return a configured Groq Llama instance (free tier, 14,400 req/day)."""
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=settings.groq_api_key,
        temperature=0.3,
    )


async def _run_chain(prompt_template, llm, prompt_args: dict) -> str:
    """
    Invoke a single LangChain chain asynchronously.

    Args:
        prompt_template: A ChatPromptTemplate instance.
        llm: The language model to invoke.
        prompt_args: Dictionary of template variables.

    Returns:
        The text content of the model response.
    """
    chain = prompt_template | llm
    result = await chain.ainvoke(prompt_args)
    return result.content


@router.post("/adapt", response_model=AdaptResponse, tags=["Adaptation"])
async def adapt(request: AdaptRequest) -> AdaptResponse:
    """
    Generate adaptive educational content tailored to a disability profile.

    **Profile → chains mapping:**
    - ``dyslexia`` / ``adhd`` → simplified only
    - ``cognitive`` → simplified + TTS script
    - ``visual_impairment`` → visual description + TTS script
    - ``hearing_impairment`` → simplified + visual description
    - *(none)* → all three chains

    Selected chains run **concurrently** via ``asyncio.gather`` to minimise latency.
    Context is drawn from both the content FAISS index and the feedback index
    (``retrieve_with_feedback``). Pedagogy chunks are appended to the prompt after
    content chunks with a clear separator so the LLM treats them as teaching aids.

    Raises:
        HTTPException 404: No indexed documents found.
        HTTPException 500: LLM call failed.
    """
    docs = retrieve_with_feedback(request.query, chapter=request.chapter)
    if not docs:
        raise HTTPException(
            status_code=404,
            detail=(
                "No relevant content found. "
                "Please ingest educational PDFs first via POST /ingest."
            ),
        )

    content_context = "\n\n".join(doc.page_content for doc in docs)
    sources = list({doc.metadata.get("source", "unknown") for doc in docs})

    # Pedagogy analogies are only useful for STEM — skip for humanities subjects
    _STEM = {"science", "mathematics", "physics", "chemistry", "biology",
             "computer science", "maths", "math", "environmental science"}
    use_pedagogy = (
        request.subject is None
        or request.subject.strip().lower() in _STEM
    )
    pedagogy_docs = retrieve_pedagogy(request.query, k=3) if use_pedagogy else []
    pedagogy_context = "\n\n".join(doc.page_content for doc in pedagogy_docs)

    prompt_args = {
        "context": content_context,
        "pedagogy": pedagogy_context,
        "query": request.query,
    }

    llm = _get_llm()
    chains_to_run: List[str] = PROFILE_CHAINS.get(
        request.disability_profile, PROFILE_CHAINS[None]
    )

    # Build async tasks for selected chains only
    task_keys = list(chains_to_run)
    tasks = [
        _run_chain(_CHAIN_PROMPTS[key], llm, prompt_args)
        for key in task_keys
    ]

    try:
        results = await asyncio.gather(*tasks)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"LLM call failed: {exc}"
        ) from exc

    result_map = dict(zip(task_keys, results))

    return AdaptResponse(
        simplified=result_map.get("simplified"),
        visual_description=result_map.get("visual_description"),
        tts_script=result_map.get("tts_script"),
        sources=sources,
    )
