"""
Root-level conftest: set env vars BEFORE any app module is imported,
and mock out the pedagogy store build so tests do not hit the Google API
during the FastAPI lifespan startup.
"""

import os

# Must be set before any import of config.py or app modules
os.environ.setdefault("GOOGLE_API_KEY", "test-api-key")
os.environ.setdefault("FAISS_INDEX_PATH", "./test_faiss_store")
os.environ.setdefault("FAISS_FEEDBACK_PATH", "./test_faiss_feedback_store")
os.environ.setdefault("FAISS_PEDAGOGY_PATH", "./test_faiss_pedagogy_store")

from unittest.mock import patch  # noqa: E402

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def mock_lifespan_builds():
    """Prevent pedagogy store construction from running during test startup."""
    with patch("main.build_pedagogy_store"):
        yield
