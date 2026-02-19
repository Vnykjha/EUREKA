"""Router for POST /ingest — PDF ingestion endpoint."""

from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from rag.ingestor import ingest_pdf
from schemas import IngestResponse

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse, tags=["Ingestion"])
async def ingest(
    file: UploadFile = File(...),
    grade: Optional[int] = Form(None),
    subject: Optional[str] = Form(None),
    chapter: Optional[str] = Form(None),
) -> IngestResponse:
    """
    Ingest an educational PDF into the FAISS vector store.

    Accepts a multipart/form-data PDF upload plus optional curriculum metadata
    (grade, subject, chapter). Metadata is attached to every chunk so retrieval
    can later be filtered to a specific chapter.

    Raises:
        HTTPException 400: If the uploaded file is not a PDF or is empty.
        HTTPException 500: If the ingestion pipeline fails.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        chunks_indexed = ingest_pdf(
            file_bytes, file.filename,
            grade=grade, subject=subject, chapter=chapter,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Ingestion failed: {exc}"
        ) from exc

    return IngestResponse(
        status="success",
        chunks_indexed=chunks_indexed,
        filename=file.filename,
    )
