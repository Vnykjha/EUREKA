"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rag.pedagogy_store import build_pedagogy_store
from routers import adapt, concept_graph, feedback, ingest


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build vector stores at startup if they don't already exist."""
    try:
        build_pedagogy_store()
    except Exception as exc:  # noqa: BLE001
        print(f"[WARNING] Could not build pedagogy store at startup: {exc}")
    yield


app = FastAPI(
    title="Inclusive Multimodal Learning API",
    description=(
        "A RAG-powered backend that adapts educational content for students "
        "with diverse learning needs (Track 3B)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(adapt.router)
app.include_router(feedback.router)
app.include_router(concept_graph.router)


@app.get("/", tags=["Health"])
async def root() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "service": "Inclusive Multimodal Learning API"}


@app.get("/ui", tags=["UI"], include_in_schema=False)
async def serve_ui() -> FileResponse:
    """Serve the sample frontend UI."""
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/voice", tags=["UI"], include_in_schema=False)
async def serve_voice() -> FileResponse:
    """Serve the voice-controlled UI for visual impairment mode."""
    return FileResponse(Path(__file__).parent / "static" / "voice.html")
