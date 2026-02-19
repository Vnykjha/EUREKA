"""
Endpoint tests for the Inclusive Multimodal Learning API.

Uses pytest-asyncio + httpx.AsyncClient with ASGITransport so no live server
is required. External calls (FAISS, LLM) are mocked throughout.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from langchain_core.documents import Document

from main import app
from schemas import AdaptResponse, ConceptGraphResponse, FeedbackResponse, IngestResponse


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_pdf_bytes() -> bytes:
    """Minimal valid single-page PDF for upload tests."""
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << >> >>\nendobj\n"
        b"4 0 obj\n<< /Length 44 >>\nstream\n"
        b"BT /F1 12 Tf 100 700 Td (Test) Tj ET\nendstream\nendobj\n"
        b"xref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n"
        b"0000000058 00000 n\n0000000115 00000 n\n0000000266 00000 n\n"
        b"trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n360\n%%EOF"
    )


@pytest.fixture
def sample_docs() -> list:
    """Sample retrieved documents for mocking retriever calls."""
    return [
        Document(
            page_content="Photosynthesis converts sunlight into glucose.",
            metadata={"source": "biology.pdf"},
        )
    ]


@pytest.fixture
def pedagogy_docs() -> list:
    """Sample pedagogy documents for mocking pedagogy retrieval."""
    return [
        Document(
            page_content="ELI5: A plant is like a tiny solar kitchen.",
            metadata={"topic": "photosynthesis", "type": "pedagogy"},
        )
    ]


# ---------------------------------------------------------------------------
# POST /ingest
# ---------------------------------------------------------------------------

async def test_ingest_pdf_success(sample_pdf_bytes):
    """Valid PDF upload should return status=success with chunk count."""
    with patch("routers.ingest.ingest_pdf", return_value=5) as mock_ingest:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/ingest",
                files={"file": ("lesson.pdf", sample_pdf_bytes, "application/pdf")},
            )

    assert response.status_code == 200
    data = IngestResponse(**response.json())
    assert data.status == "success"
    assert data.chunks_indexed == 5
    assert data.filename == "lesson.pdf"
    mock_ingest.assert_called_once()


async def test_ingest_non_pdf_rejected():
    """Non-PDF upload should return HTTP 400."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/ingest",
            files={"file": ("notes.txt", b"hello", "text/plain")},
        )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# POST /adapt
# ---------------------------------------------------------------------------

async def test_adapt_returns_all_fields_no_profile(sample_docs, pedagogy_docs):
    """Without a disability profile all three chains should be invoked."""
    with (
        patch("routers.adapt.retrieve_with_feedback", return_value=sample_docs),
        patch("routers.adapt.retrieve_pedagogy", return_value=pedagogy_docs),
        patch("routers.adapt._run_chain", new_callable=AsyncMock, return_value="OK"),
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/adapt", json={"query": "What is photosynthesis?"}
            )

    assert response.status_code == 200
    data = AdaptResponse(**response.json())
    assert data.simplified == "OK"
    assert data.visual_description == "OK"
    assert data.tts_script == "OK"


async def test_adapt_dyslexia_profile_runs_one_chain(sample_docs, pedagogy_docs):
    """dyslexia profile should invoke only the simplified chain (call count = 1)."""
    call_count = 0

    async def counting_chain(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        return "Simplified text"

    with (
        patch("routers.adapt.retrieve_with_feedback", return_value=sample_docs),
        patch("routers.adapt.retrieve_pedagogy", return_value=pedagogy_docs),
        patch("routers.adapt._run_chain", side_effect=counting_chain),
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/adapt",
                json={"query": "Explain gravity", "disability_profile": "dyslexia"},
            )

    assert response.status_code == 200
    assert call_count == 1


async def test_adapt_cognitive_profile_runs_two_chains(sample_docs, pedagogy_docs):
    """cognitive profile should invoke simplified + tts_script (call count = 2)."""
    call_count = 0

    async def counting_chain(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        return "Result"

    with (
        patch("routers.adapt.retrieve_with_feedback", return_value=sample_docs),
        patch("routers.adapt.retrieve_pedagogy", return_value=pedagogy_docs),
        patch("routers.adapt._run_chain", side_effect=counting_chain),
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/adapt",
                json={"query": "Explain circuits", "disability_profile": "cognitive"},
            )

    assert response.status_code == 200
    assert call_count == 2


async def test_adapt_missing_query_returns_422():
    """POST /adapt with an empty body should return HTTP 422."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/adapt", json={})
    assert response.status_code == 422


async def test_adapt_404_when_no_documents_indexed():
    """POST /adapt when retriever returns empty list should return HTTP 404."""
    with patch("routers.adapt.retrieve_with_feedback", return_value=[]):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/adapt", json={"query": "What is mitosis?"}
            )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /feedback
# ---------------------------------------------------------------------------

async def test_feedback_low_rating_is_indexed():
    """Rating ≤ 3 should trigger upsert and return indexed=True."""
    with patch("routers.feedback.upsert_feedback") as mock_upsert:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/feedback",
                json={
                    "query": "Explain gravity",
                    "adapted_content": "Gravity pulls objects.",
                    "rating": 2,
                    "disability_profile": "adhd",
                },
            )

    assert response.status_code == 200
    data = FeedbackResponse(**response.json())
    assert data.status == "received"
    assert data.indexed is True
    mock_upsert.assert_called_once()


async def test_feedback_high_rating_not_indexed():
    """Rating > 3 should NOT call upsert and return indexed=False."""
    with patch("routers.feedback.upsert_feedback") as mock_upsert:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/feedback",
                json={
                    "query": "Explain gravity",
                    "adapted_content": "Great explanation!",
                    "rating": 5,
                    "disability_profile": "dyslexia",
                },
            )

    assert response.status_code == 200
    data = FeedbackResponse(**response.json())
    assert data.indexed is False
    mock_upsert.assert_not_called()


async def test_feedback_invalid_rating_returns_422():
    """Rating outside 1–5 range should return HTTP 422."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/feedback",
            json={
                "query": "test",
                "adapted_content": "content",
                "rating": 10,
                "disability_profile": "adhd",
            },
        )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /concept-graph
# ---------------------------------------------------------------------------

async def test_concept_graph_returns_valid_structure():
    """Valid content should return a graph with nodes and edges."""
    mock_json = json.dumps(
        {
            "nodes": [
                {"id": "photosynthesis", "label": "Photosynthesis"},
                {"id": "sunlight", "label": "Sunlight"},
            ],
            "edges": [
                {"from": "sunlight", "to": "photosynthesis", "relation": "requires"}
            ],
        }
    )
    mock_result = MagicMock()
    mock_result.content = mock_json

    with patch(
        "routers.concept_graph.ChatGoogleGenerativeAI.ainvoke",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/concept-graph",
                json={"content": "Plants use sunlight for photosynthesis."},
            )

    assert response.status_code == 200
    data = response.json()
    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1


async def test_concept_graph_missing_content_returns_422():
    """POST /concept-graph without content should return HTTP 422."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/concept-graph", json={})
    assert response.status_code == 422
