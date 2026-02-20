"""FAISS retrieval with dual-index (content + feedback) support."""

import os
from typing import List, Optional

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from config import settings


def _get_embeddings() -> HuggingFaceEmbeddings:
    """Return local sentence-transformers embeddings (no API quota used)."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def _load_index(path: str) -> Optional[FAISS]:
    """Load a FAISS index from disk; return None if the path does not exist."""
    if not os.path.exists(path):
        return None
    return FAISS.load_local(
        path,
        _get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def retrieve(query: str, k: int = 5, chapter: Optional[str] = None) -> List[Document]:
    """
    Search the main content FAISS index.

    If ``chapter`` is provided, returns only chunks tagged with that chapter.
    Does NOT fall back to unfiltered search when chapter is specified — returning
    unrelated chunks produces worse output than letting the LLM use its own knowledge.

    Args:
        query: The search query string.
        k: Maximum number of results to return.
        chapter: Optional chapter title to filter results.

    Returns:
        List of relevant Document objects, empty if index does not exist or no
        matching chunks found for the given chapter filter.
    """
    index = _load_index(settings.faiss_index_path)
    if index is None:
        return []
    if chapter:
        # Only return chunks that actually belong to this chapter.
        # If none are found (PDF not ingested), return [] so the caller can
        # fall back to LLM parametric knowledge instead of wrong content.
        return index.similarity_search(query, k=k, filter={"chapter": chapter})
    return index.similarity_search(query, k=k)


def upsert_feedback(query: str, adapted_content: str) -> None:
    """
    Embed and store a low-rated query/response pair in the feedback index.

    Args:
        query: The original student query.
        adapted_content: The adapted response that received a low rating.
    """
    embeddings = _get_embeddings()
    doc = Document(
        page_content=f"Query: {query}\nAdapted Content: {adapted_content}",
        metadata={"type": "feedback"},
    )
    index_path = settings.faiss_feedback_path

    if os.path.exists(index_path):
        existing = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        existing.add_documents([doc])
        existing.save_local(index_path)
    else:
        new_index = FAISS.from_documents([doc], embeddings)
        new_index.save_local(index_path)


def retrieve_with_feedback(
    query: str, k: int = 5, chapter: Optional[str] = None
) -> List[Document]:
    """
    Search both the content index and the feedback index, then merge results.

    Deduplicates by page_content so the LLM never receives duplicate chunks.
    Passes the chapter filter to the content index search.

    Args:
        query: The search query string.
        k: Number of results requested from each index.
        chapter: Optional chapter title to filter content index results.

    Returns:
        Deduplicated list of relevant Document objects.
    """
    content_docs = retrieve(query, k=k, chapter=chapter)

    feedback_index = _load_index(settings.faiss_feedback_path)
    feedback_docs = (
        feedback_index.similarity_search(query, k=k)
        if feedback_index is not None
        else []
    )

    seen: set = set()
    merged: List[Document] = []
    for doc in content_docs + feedback_docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            merged.append(doc)

    return merged
