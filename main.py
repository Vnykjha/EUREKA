"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from rag.pedagogy_store import build_pedagogy_store
from routers import adapt, auth, concept_graph, feedback, flashcard, ingest, quiz


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
app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(flashcard.router)

# Serve static assets (JS, CSS, images)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


@app.get("/", tags=["Health"])
async def root() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "service": "Inclusive Multimodal Learning API"}


@app.get("/ui", tags=["UI"], include_in_schema=False)
async def serve_ui() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/login", tags=["UI"], include_in_schema=False)
async def serve_login() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "login.html")


@app.get("/student", tags=["UI"], include_in_schema=False)
async def serve_student() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "student.html")


@app.get("/teacher", tags=["UI"], include_in_schema=False)
async def serve_teacher() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "teacher.html")


@app.get("/learn", tags=["UI"], include_in_schema=False)
async def serve_learn() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "learn" / "index.html")


@app.get("/learn/adhd", tags=["UI"], include_in_schema=False)
async def serve_adhd() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "learn" / "adhd.html")


@app.get("/learn/dyslexia", tags=["UI"], include_in_schema=False)
async def serve_dyslexia() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "learn" / "dyslexia.html")


@app.get("/learn/visual", tags=["UI"], include_in_schema=False)
async def serve_visual() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "learn" / "visual.html")


@app.get("/learn/hearing", tags=["UI"], include_in_schema=False)
async def serve_hearing() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "learn" / "hearing.html")


@app.get("/learn/cognitive", tags=["UI"], include_in_schema=False)
async def serve_cognitive() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "learn" / "cognitive.html")


@app.get("/voice", tags=["UI"], include_in_schema=False)
async def serve_voice() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "voice.html")
