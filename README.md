# ⚡ EUREKA — Inclusive Multimodal Learning Platform

> **Hackathon Project · Track 3B · Team Rocket**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-orange)](https://langchain.com)
[![FAISS](https://img.shields.io/badge/Vector_Store-FAISS-red)](https://github.com/facebookresearch/faiss)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🎯 Our Aim

Education is not one-size-fits-all. Students with ADHD, dyslexia, visual impairments, hearing impairments, and cognitive differences often struggle with standard textbook content — not because they can't learn, but because the *format* doesn't work for them.

**EUREKA** is an AI-powered inclusive learning platform that takes any educational content — NCERT textbooks, custom PDFs, or video transcripts — and adapts it in real time to match each student's unique learning profile. Every student deserves to learn without limits.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📘 **NCERT Navigation** | Full curriculum flow: Board → Grade → Subject → Chapter |
| 🎯 **Disability Profile Routing** | Adapts content for ADHD, Dyslexia, Visual Impairment, Hearing Impairment, and Cognitive profiles |
| 🔍 **RAG Pipeline** | Local FAISS vector store + Retrieval-Augmented Generation for contextual answers |
| 📚 **Dual-Index RAG** | Retrieves from both ingested content AND a curated pedagogy store |
| ⚡ **Parallel LLM Calls** | `asyncio.gather` for concurrent chain execution — low latency |
| 🔄 **Feedback Loop** | Low-rated responses are indexed and used to improve future answers |
| 🧠 **Concept Dependency Graph** | Extracts concept nodes and prerequisite edges from any text |
| 📄 **PDF Ingestion** | Upload any educational PDF and query it instantly |
| 💬 **AI Teacher Chat** | Ask follow-up questions in natural language, adapted to your profile |
| 🌐 **Animated Web UI** | Beautiful dark/light themed frontend with full NCERT navigation |
| 🚧 **Coming Soon** | ICSE & State Board curriculum, video transcript ingestion (Whisper) |

---

## 🏗️ Architecture

```
Student Request
      │
      ▼
┌─────────────────────────────────────────┐
│             FastAPI Backend              │
│  ┌─────────┐  ┌────────┐  ┌──────────┐ │
│  │ /ingest │  │ /adapt │  │/feedback │ │
│  └────┬────┘  └───┬────┘  └────┬─────┘ │
│       │           │             │       │
│  ┌────▼───────────▼─────────────▼────┐  │
│  │          RAG Pipeline              │  │
│  │  FAISS Content + Pedagogy + FB    │  │
│  │  sentence-transformers embeddings │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────▼────────────────────┐  │
│  │       Groq LLM (Llama 3.1 8B)     │  │
│  │   Disability-adapted prompts      │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI + Uvicorn |
| **LLM** | Groq API (Llama 3.1 8B Instant) — free tier, 14,400 req/day |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` — **runs locally, zero API cost** |
| **Vector Store** | FAISS (content, feedback, pedagogy indexes) |
| **PDF Parsing** | LangChain PyPDFLoader |
| **RAG Framework** | LangChain 0.2+ |
| **Frontend** | Vanilla HTML/CSS/JS — animated, responsive, dark/light theme |
| **Testing** | pytest + httpx (mocked) |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ingest` | Upload a PDF → index into FAISS |
| `POST` | `/adapt` | Get disability-adapted content for a query |
| `POST` | `/feedback` | Rate a response; low ratings improve future answers |
| `POST` | `/concept-graph` | Extract concept dependency graph from text |
| `GET` | `/ui` | Serve the interactive web frontend |
| `GET` | `/docs` | Swagger UI — interactive API documentation |

### POST /adapt — Request Body
```json
{
  "query": "What led to the rise of Hitler?",
  "disability_profile": "adhd",
  "image_base64": null
}
```

**Supported `disability_profile` values:**
- `"adhd"` → Simplified, bullet-point-friendly content
- `"dyslexia"` → Simple language, short sentences
- `"visual_impairment"` → Detailed visual descriptions + TTS script
- `"hearing_impairment"` → Text-rich, visual-focused content
- `"cognitive"` → ELI5 (Explain Like I'm 5) style + TTS
- *(omit)* → All output types returned

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Groq API Key](https://console.groq.com) (free)

### 1. Clone the repo
```bash
git clone https://github.com/Vnykjha/EUREKA.git
cd EUREKA
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env and add your Groq API key:
# GROQ_API_KEY=gsk_...
```

### 5. Run the server
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### 6. Open the app
- **Web UI:** http://127.0.0.1:8000/ui
- **API Docs:** http://127.0.0.1:8000/docs

> **Note:** On first run, the `all-MiniLM-L6-v2` embedding model (~90 MB) will be downloaded automatically. This is a one-time download.

---

## 📁 Project Structure

```
EUREKA/
├── main.py                  # FastAPI app entry point
├── config.py                # Settings via pydantic-settings
├── schemas.py               # Pydantic request/response models
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
│
├── rag/
│   ├── ingestor.py          # PDF → chunks → FAISS indexing
│   ├── retriever.py         # FAISS retrieval (content + feedback)
│   ├── pedagogy_store.py    # Pre-built teaching analogies store
│   └── prompts.py           # LLM prompt templates
│
├── routers/
│   ├── ingest.py            # POST /ingest
│   ├── adapt.py             # POST /adapt (parallel LLM chains)
│   ├── feedback.py          # POST /feedback
│   └── concept_graph.py     # POST /concept-graph
│
├── static/
│   └── index.html           # Animated web frontend
│
└── tests/
    └── test_endpoints.py    # pytest test suite (all endpoints mocked)
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🗺️ Roadmap

- [x] PDF ingestion + FAISS RAG pipeline
- [x] Disability profile routing (5 profiles)
- [x] Parallel LLM calls with asyncio
- [x] Feedback loop with low-rating indexing
- [x] Concept dependency graph endpoint
- [x] Animated web frontend with NCERT navigation
- [x] Dark / Light theme toggle
- [ ] Video ingestion with Whisper transcription
- [ ] ICSE and State Board curriculum
- [ ] Semantic response cache
- [ ] Student progress tracking

---

## 👥 Team Rocket

Built with ❤️ for the Eurekathon Hackathon · Track 3B: Inclusive Education

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
