"""Router for POST /concept-graph — concept dependency graph generation."""

import json
import re

from fastapi import APIRouter, HTTPException
from langchain_groq import ChatGroq

from config import settings
from schemas import ConceptGraphRequest, ConceptGraphResponse

router = APIRouter()

_CONCEPT_GRAPH_PROMPT = """\
Analyse the educational content below and extract key concepts with their dependencies.

Return ONLY a valid JSON object with this exact structure — no markdown fences, no explanation:
{{
  "nodes": [
    {{"id": "concept_id", "label": "Human Readable Name"}}
  ],
  "edges": [
    {{"from": "prerequisite_id", "to": "dependent_id", "relation": "requires"}}
  ]
}}

Rules:
- Node IDs must be lowercase with underscores (e.g. "newtons_first_law")
- An edge from A to B means: you must understand A before B
- Include 5–15 nodes and all meaningful prerequisite relationships
- Omit trivial or redundant edges

Educational Content:
{content}
"""


def _get_llm() -> ChatGroq:
    """Return a configured Groq Llama instance (low temperature for structured output)."""
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=settings.groq_api_key,
        temperature=0.1,
    )


@router.post(
    "/concept-graph",
    response_model=ConceptGraphResponse,
    response_model_by_alias=True,
    tags=["Analysis"],
)
async def concept_graph(request: ConceptGraphRequest) -> ConceptGraphResponse:
    """
    Generate a concept dependency graph from raw educational text.

    Uses a single Gemini LLM call with a structured JSON prompt. The returned
    graph contains nodes (concepts) and directed edges representing prerequisite
    relationships — suitable for direct rendering by a React/D3 frontend without
    any server-side graph library.

    Args:
        request: ConceptGraphRequest with the raw lesson text.

    Returns:
        ConceptGraphResponse with ``nodes`` and ``edges`` lists.

    Raises:
        HTTPException 500: LLM call failed or returned invalid JSON.
        HTTPException 422: JSON parsed but failed Pydantic schema validation.
    """
    llm = _get_llm()
    prompt = _CONCEPT_GRAPH_PROMPT.format(content=request.content)

    try:
        result = await llm.ainvoke(prompt)
        raw = result.content.strip()
        # Strip markdown code fences if the model wraps its output
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500, detail=f"LLM returned invalid JSON: {exc}"
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Concept graph generation failed: {exc}"
        ) from exc

    try:
        return ConceptGraphResponse(**data)
    except Exception as exc:
        raise HTTPException(
            status_code=422, detail=f"Graph schema validation failed: {exc}"
        ) from exc
