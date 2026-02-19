"""Pre-populated pedagogy FAISS store with teaching analogies and ELI5 explanations."""

import os
from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from config import settings

PEDAGOGY_ENTRIES: List[dict] = [
    {
        "topic": "photosynthesis",
        "content": (
            "ELI5 — Photosynthesis: A plant is like a tiny solar-powered kitchen. "
            "Leaves are solar panels that catch sunlight. The plant mixes sunlight with "
            "water (from soil) and carbon dioxide (from air) to make its own food — sugar. "
            "Analogy: Like baking a cake, but you use sunlight instead of an oven."
        ),
    },
    {
        "topic": "fractions",
        "content": (
            "ELI5 — Fractions: Picture a pizza cut into 8 equal slices. If you eat 3, "
            "you ate 3/8 of the pizza. The bottom number (denominator) = how many equal "
            "pieces the whole is cut into. The top number (numerator) = how many you have."
        ),
    },
    {
        "topic": "Newton's first law",
        "content": (
            "Analogy — Newton's First Law (Inertia): A ball on a smooth table won't move "
            "unless you push it. Once rolling, it keeps rolling forever unless friction or "
            "a wall stops it. Objects are 'lazy' — they resist any change to their current state."
        ),
    },
    {
        "topic": "Newton's second law",
        "content": (
            "Analogy — Newton's Second Law (F=ma): Pushing an empty shopping cart is easy "
            "(low mass). A full one is harder (high mass). Push harder → accelerates faster. "
            "F=ma: Force = mass × acceleration."
        ),
    },
    {
        "topic": "Newton's third law",
        "content": (
            "Analogy — Newton's Third Law: When you sit in a chair, your body pushes down; "
            "the chair pushes back up with equal force — that's why you don't fall through. "
            "Every push has an equal push back in the opposite direction."
        ),
    },
    {
        "topic": "electric circuits",
        "content": (
            "Analogy — Electric Circuits: Electricity is like water in pipes. "
            "Voltage = water pressure. Current = how much water flows per second. "
            "Resistance = how narrow the pipe is. A battery is the water pump."
        ),
    },
    {
        "topic": "gravity",
        "content": (
            "ELI5 — Gravity: Every object with mass pulls every other object toward it — "
            "like invisible magnets. Earth is huge so it pulls everything toward its centre. "
            "That's why dropped objects fall down. The Moon's pull on Earth causes ocean tides."
        ),
    },
    {
        "topic": "DNA and genetics",
        "content": (
            "Analogy — DNA: DNA is an instruction manual for building a living thing. "
            "Each cell holds a full copy of the manual. Genes are individual chapters, "
            "each describing one trait (like eye colour). The four DNA letters (A, T, C, G) "
            "are the alphabet the manual is written in."
        ),
    },
    {
        "topic": "water cycle",
        "content": (
            "ELI5 — The Water Cycle: Water goes on an endless journey. "
            "Heat evaporates water from oceans into vapour that rises. "
            "High up it cools and condenses into clouds. It falls as rain or snow (precipitation) "
            "and collects in rivers and oceans. Then the cycle repeats — like a giant recycling loop."
        ),
    },
    {
        "topic": "supply and demand",
        "content": (
            "Analogy — Supply and Demand: 10 concert tickets, 100 people want them → "
            "high demand, low supply → price rises. 1000 tickets, 50 people want them → "
            "low demand, high supply → price falls. Markets adjust prices until buyers and sellers agree."
        ),
    },
    {
        "topic": "cells",
        "content": (
            "Analogy — Cells: A cell is like a tiny city. The nucleus = city hall (holds the DNA plans). "
            "Mitochondria = power plants (generate energy). Cell membrane = city wall (controls entry/exit). "
            "Ribosomes = factories (build proteins)."
        ),
    },
]


def _get_embeddings() -> HuggingFaceEmbeddings:
    """Return local sentence-transformers embeddings (no API quota used)."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def build_pedagogy_store() -> None:
    """
    Build the pedagogy FAISS store from hardcoded entries.

    Skips silently if the store already exists on disk.
    """
    index_path = settings.faiss_pedagogy_path
    if os.path.exists(index_path):
        return

    docs = [
        Document(
            page_content=entry["content"],
            metadata={"topic": entry["topic"], "type": "pedagogy"},
        )
        for entry in PEDAGOGY_ENTRIES
    ]
    index = FAISS.from_documents(docs, _get_embeddings())
    index.save_local(index_path)


def retrieve_pedagogy(query: str, k: int = 3) -> List[Document]:
    """
    Retrieve the most relevant teaching analogies for a given query.

    Builds the store on first call if it does not yet exist.

    Args:
        query: The student question or topic phrase.
        k: Number of pedagogy chunks to retrieve.

    Returns:
        List of relevant pedagogy Document objects.
    """
    index_path = settings.faiss_pedagogy_path
    if not os.path.exists(index_path):
        build_pedagogy_store()

    index = FAISS.load_local(
        index_path,
        _get_embeddings(),
        allow_dangerous_deserialization=True,
    )
    return index.similarity_search(query, k=k)
