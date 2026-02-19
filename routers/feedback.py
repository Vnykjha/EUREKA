"""Router for POST /feedback — user feedback collection and low-rating indexing."""

from fastapi import APIRouter, HTTPException

from rag.retriever import upsert_feedback
from schemas import FeedbackRequest, FeedbackResponse

router = APIRouter()

LOW_RATING_THRESHOLD = 3


@router.post("/feedback", response_model=FeedbackResponse, tags=["Feedback"])
async def feedback(request: FeedbackRequest) -> FeedbackResponse:
    """
    Collect user feedback on adapted content.

    When ``rating`` is **3 or below**, the query + adapted content pair is
    embedded and upserted into the ``faiss_feedback_store`` index. This allows
    ``retrieve_with_feedback`` in future ``/adapt`` calls to surface previously
    poorly-rated queries as additional context, helping the LLM avoid
    repeating the same low-quality explanation pattern.

    Args:
        request: FeedbackRequest with query, content, rating (1-5), and profile.

    Returns:
        FeedbackResponse indicating whether the content was indexed.

    Raises:
        HTTPException 500: If the feedback embedding/upsert fails.
    """
    should_index = request.rating <= LOW_RATING_THRESHOLD

    if should_index:
        try:
            upsert_feedback(request.query, request.adapted_content)
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to index feedback: {exc}",
            ) from exc

    return FeedbackResponse(status="received", indexed=should_index)
