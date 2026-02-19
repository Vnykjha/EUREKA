"""Pydantic schemas for all request and response models."""

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

DisabilityProfile = Literal[
    "dyslexia",
    "visual_impairment",
    "hearing_impairment",
    "adhd",
    "cognitive",
]


class IngestResponse(BaseModel):
    """Response model for POST /ingest."""

    status: str
    chunks_indexed: int
    filename: str


class AdaptRequest(BaseModel):
    """Request model for POST /adapt."""

    query: str
    image_base64: Optional[str] = None
    disability_profile: Optional[DisabilityProfile] = None
    # Curriculum context for chapter-filtered RAG retrieval
    grade: Optional[int] = None
    subject: Optional[str] = None
    chapter: Optional[str] = None


class AdaptResponse(BaseModel):
    """Response model for POST /adapt."""

    simplified: Optional[str] = None
    visual_description: Optional[str] = None
    tts_script: Optional[str] = None
    sources: List[str] = Field(default_factory=list)


class FeedbackRequest(BaseModel):
    """Request model for POST /feedback."""

    query: str
    adapted_content: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 (poor) to 5 (excellent)")
    disability_profile: str


class FeedbackResponse(BaseModel):
    """Response model for POST /feedback."""

    status: str
    indexed: bool


class ConceptNode(BaseModel):
    """A node in the concept dependency graph."""

    id: str
    label: str


class ConceptEdge(BaseModel):
    """An edge in the concept dependency graph."""

    from_node: str = Field(..., alias="from")
    to: str
    relation: str = "requires"

    model_config = ConfigDict(populate_by_name=True)


class ConceptGraphRequest(BaseModel):
    """Request model for POST /concept-graph."""

    content: str


class ConceptGraphResponse(BaseModel):
    """Response model for POST /concept-graph."""

    nodes: List[ConceptNode]
    edges: List[ConceptEdge]
