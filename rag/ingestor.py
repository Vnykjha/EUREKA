"""PDF ingestion and FAISS index building."""

import os
import tempfile
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings


def _get_embeddings() -> HuggingFaceEmbeddings:
    """Return local sentence-transformers embeddings (no API quota used)."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def ingest_pdf(
    file_bytes: bytes,
    filename: str,
    grade: Optional[int] = None,
    subject: Optional[str] = None,
    chapter: Optional[str] = None,
) -> int:
    """
    Ingest a PDF into the local FAISS vector store.

    Curriculum metadata (grade, subject, chapter) is attached to every chunk
    so that retrieval can be filtered to a specific chapter later.

    Args:
        file_bytes: Raw PDF bytes.
        filename: Original filename (stored as chunk metadata).
        grade: NCERT grade number (1-12), optional.
        subject: Subject name (e.g. "Science"), optional.
        chapter: Chapter title for exact-match filtering, optional.

    Returns:
        Number of chunks indexed.
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = filename
            if grade is not None:
                doc.metadata["grade"] = grade
            if subject:
                doc.metadata["subject"] = subject
            if chapter:
                doc.metadata["chapter"] = chapter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        chunks = splitter.split_documents(documents)

        embeddings = _get_embeddings()
        index_path = settings.faiss_index_path

        if os.path.exists(index_path):
            existing = FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True,
            )
            existing.add_documents(chunks)
            existing.save_local(index_path)
        else:
            new_index = FAISS.from_documents(chunks, embeddings)
            new_index.save_local(index_path)

        return len(chunks)
    finally:
        os.unlink(tmp_path)
