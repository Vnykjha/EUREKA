# EUREKA — Complete Pitch Guide

---

## 1. WHAT IS EUREKA?

**EUREKA** is an AI-powered inclusive learning platform that adapts educational content in real time for students with diverse learning needs — ADHD, dyslexia, cognitive disabilities, visual impairment, and hearing impairment.

Instead of one-size-fits-all textbooks, EUREKA takes any NCERT chapter and transforms it into a format specifically engineered for each disability profile, delivered through a beautiful, accessible web interface.

**Tagline:** *Learn Without Limits.*

---

## 2. THE PROBLEM

- 1 in 5 students worldwide has a learning disability.
- India has ~8 million students with special needs in mainstream schools.
- Standard textbooks and classroom delivery are inaccessible for most of them.
- Existing assistive tools are either expensive, isolated apps, or not curriculum-aligned.
- Teachers lack the time/training to manually adapt content for every student.

**EUREKA solves all of this — automatically, in seconds, for free.**

---

## 3. SYSTEM ARCHITECTURE (Big Picture)

```
Student logs in → Selects profile (ADHD / Dyslexia / etc.)
       ↓
Selects Grade + Subject + Chapter
       ↓
Frontend sends POST /adapt to FastAPI backend
       ↓
RAG pipeline: FAISS vector search → retrieves relevant chunks from ingested PDFs
       ↓
If no PDF ingested → LLM uses its own NCERT knowledge (fallback)
       ↓
LangChain prompt (profile-specific) → Groq LLM (Llama 3.1 8B Instant)
       ↓
Structured adapted content returned → Profile-specific HTML page renders it
       ↓
Student interacts: checkpoints / quiz / flashcards / TTS / visual descriptions
```

---

## 4. TECH STACK

| Layer | Technology | Why |
|---|---|---|
| Backend | **FastAPI** (Python) | Async, fast, auto-docs |
| LLM | **Groq + Llama 3.1 8B Instant** | Free tier, <1s inference |
| Orchestration | **LangChain** | Prompt templating, chain composition |
| Vector DB | **FAISS** (local) | No cost, fast similarity search |
| Embeddings | **HuggingFace sentence-transformers** | Free, runs locally |
| Frontend | **Vanilla JS + HTML/CSS** | Zero dependencies, fast load |
| Auth | **JWT tokens** (localStorage) | Stateless, simple |
| PDF Ingestion | **PyMuPDF / LangChain** loaders | Extract text from NCERT PDFs |

---

## 5. CORE FEATURES — HOW EACH WORKS

### 5.1 RAG Pipeline (Retrieval-Augmented Generation)

**Files:** `rag/ingestor.py`, `rag/retriever.py`, `faiss_store/`

- When a teacher uploads a PDF (`POST /ingest`), it is chunked into ~500-token segments
- Each chunk is embedded using a sentence-transformer and stored in FAISS with metadata (`chapter`, `grade`, `subject`, `source`)
- At query time, `retriever.py` does similarity search **filtered by chapter** so no cross-contamination
- **Smart fallback:** if no PDF is ingested for that chapter, the LLM is instructed to use its own NCERT knowledge with a strict instruction not to hallucinate from other chapters

### 5.2 Disability Profile Routing

**File:** `routers/adapt.py`

Each profile maps to specific LangChain chains:

| Profile | Chains Run | Output Field |
|---|---|---|
| `adhd` | `adhd_simplified` | `simplified` |
| `dyslexia` | `simplified` | `simplified` |
| `cognitive` | `simplified` + `tts_script` | `simplified` + `tts_script` |
| `visual_impairment` | `visual_description` + `tts_script` | `visual_description` + `tts_script` |
| `hearing_impairment` | `simplified` + `visual_description` | both fields |

Multiple chains run **concurrently** via `asyncio.gather` — no sequential waiting.

### 5.3 ADHD Mode — Chunk + Checkpoint Flow

**Files:** `rag/prompts.py` (ADHD_PROMPT), `static/learn/adhd.html`

The LLM is instructed to output content as 3 sections using `[SECTION]` / `[CHECKPOINT]` markers:

```
[SECTION]
Heading: Early Life of Hitler
- 🏠 **Birthplace**: Hitler was born in Braunau, Austria.
- 👨‍👩‍👧 **Family**: His father was a customs officer.
...

[CHECKPOINT]
Q: Where was Hitler born?
a) Germany | b) Austria | c) France | d) Italy
ANS: b
```

The frontend parser splits on these markers, renders one section at a time (others locked), and after all bullets are checked → inline MCQ checkpoint appears → correct/wrong feedback → next section unlocks. This mimics spaced repetition and prevents cognitive overload.

### 5.4 Pedagogy Store

**Files:** `rag/pedagogy_store.py`, `faiss_pedagogy_store/`

A separate FAISS index containing **teaching analogies and pedagogical strategies** (Bloom's Taxonomy, Feynman Technique examples, etc.). These are retrieved alongside content and injected into the prompt as "teaching aids" — so the LLM doesn't just summarise but actually teaches effectively. Only used for STEM subjects (skipped for humanities to reduce noise).

### 5.5 Quiz Generation

**Endpoint:** `POST /quiz/generate`  
Takes the raw adapted content, asks the LLM to generate 5 MCQs, returns JSON. Student answers are tracked and submitted to `POST /quiz/submit` which saves to `quiz_results.json`.

### 5.6 Flashcard Generation

**Endpoint:** `POST /flashcard/generate`  
LLM generates Q&A pairs from the content. Rendered as 3D flip cards in the browser.

### 5.7 Auth Flow

**File:** `routers/auth.py`, `users.json`

- Simple JWT-based auth with role (`student` / `teacher`)
- Tokens stored in `localStorage`
- Students → `/student`, Teachers → `/teacher`
- All learn pages check for token on load; redirect to `/login` if missing

### 5.8 Teacher Dashboard

**File:** `static/teacher.html`

- View quiz results per student/chapter
- Upload PDFs for ingestion
- See concept graphs (dependency maps between topics)

### 5.9 Concept Graph

**Endpoint:** `POST /concept_graph`  
Generates a JSON graph of concept dependencies for a chapter (e.g., "Electricity" → needs "Charge" → needs "Atoms"). Useful for teachers to understand prerequisite gaps.

### 5.10 Feedback Loop

**Endpoint:** `POST /feedback`  
Student ratings are stored and re-indexed as low-weight vectors in FAISS — so future retrievals for the same chapter slightly favour content students found helpful.

---

## 6. FRONTEND PAGES

| URL | Page | Purpose |
|---|---|---|
| `/login` | login.html | Sign in / sign up, role select |
| `/student` | student.html | Coverflow mode selector |
| `/learn/adhd` | adhd.html | ADHD chunk+checkpoint mode |
| `/learn/dyslexia` | dyslexia.html | Simplified large-text mode |
| `/learn/cognitive` | cognitive.html | Simplified + audio script |
| `/learn/visual` | visual.html | Audio descriptions + TTS |
| `/learn/hearing` | hearing.html | Simplified + visual diagrams |
| `/teacher` | teacher.html | Teacher dashboard |

---

## 7. DATA FLOW WALKTHROUGH (End-to-End)

1. Teacher uploads NCERT PDF → `POST /ingest` → chunked → embedded → stored in FAISS
2. Student logs in → JWT token stored
3. Student selects ADHD mode on `/student` → routed to `/learn/adhd`
4. Student selects Grade 9, Social Science, "Nazism and Rise of Hitler" → clicks Load
5. Frontend posts to `POST /adapt` with `disability_profile: "adhd"`
6. Backend retrieves top-k chunks filtered to that chapter from FAISS
7. ADHD_PROMPT + chunks → Groq LLM → structured `[SECTION]/[CHECKPOINT]` output
8. Frontend parser splits into 3 chunks, renders Section 1 unlocked
9. Student reads, checks all bullets → "I've read this" button → inline MCQ appears
10. Student answers → feedback → Section 2 unlocks → repeat
11. After Section 3 → Final Quiz + Flashcards appear
12. Quiz score submitted → stored in `quiz_results.json` → visible on teacher dashboard

---

## 8. JUDGE QUESTIONS & ANSWERS

---

### TECHNICAL QUESTIONS

**Q1: Why did you choose FAISS over a cloud vector DB like Pinecone?**

> FAISS runs entirely locally — zero cost, zero latency overhead from network calls, and no data leaves the system. For a school setting handling student data, this is actually a privacy advantage. If we scale, we can swap to Pinecone or Weaviate since LangChain abstracts the vector store interface.

---

**Q2: How do you prevent the LLM from hallucinating content from the wrong chapter?**

> Two layers: (1) The FAISS retrieval is filtered by `chapter` metadata — only chunks tagged to that chapter are returned. (2) The prompt explicitly instructs the LLM: *"Do NOT invent content from other chapters or grades."* If no PDF exists, we tell it exactly which NCERT class/subject/chapter to draw from. Before this fix, the system was returning Class 6 content for a Class 9 query — we caught and fixed this.

---

**Q3: What is the latency of a typical /adapt request?**

> Groq's Llama 3.1 8B Instant runs at ~500 tokens/second. A typical ADHD response is ~400 tokens, so generation is under 1 second. Combined with FAISS retrieval (~10ms) and network, total round-trip is typically 1.5–3 seconds. Multiple chains (e.g., cognitive profile runs 2 chains) run concurrently via `asyncio.gather` so they don't add latency linearly.

---

**Q4: How does your RAG actually improve over just prompting the LLM directly?**

> Without RAG, the LLM gives generic answers based on its training data which may be outdated, incomplete, or from non-NCERT sources. With RAG, we ground the response in the exact text the teacher uploaded — so if a teacher adds supplementary notes, worked examples, or regional language pointers, those become part of the content. This also means the system works for non-standard curricula, not just NCERT.

---

**Q5: Your auth uses localStorage for JWTs — isn't that a security risk?**

> For a prototype/hackathon context, yes we acknowledge this. In production we'd use `httpOnly` cookies to prevent XSS attacks from accessing the token. The current implementation is intentionally simple to focus on the core adaptive learning functionality, not auth infrastructure.

---

**Q6: How does the pedagogy store differ from the content store?**

> The content store contains the actual chapter text (what to teach). The pedagogy store contains **how to teach** — analogies like "think of current as water flowing through a pipe", Bloom's Taxonomy prompts, Feynman technique examples. Both are retrieved and injected into the prompt separately, so the LLM can explain concepts using pedagogically proven techniques rather than just summarising the textbook.

---

**Q7: What happens if the LLM doesn't follow your [SECTION]/[CHECKPOINT] format?**

> The parser has a fallback: if no `[SECTION]` markers are found, the entire response is treated as one unlocked chunk of bullet points. This guarantees the student always sees content even if the LLM deviates from the format. In practice, Llama 3.1 follows the format reliably when given strict instructions — we also explicitly tell it *"Do NOT use ## anywhere"* to prevent the previous marker issue.

---

**Q8: Why Llama 3.1 8B and not GPT-4?**

> Three reasons: (1) Cost — Groq's free tier gives 14,400 requests/day at zero cost. (2) Speed — Llama 3.1 8B on Groq is faster than GPT-4 API. (3) Privacy — for a student data platform, keeping inference within a controlled provider is preferable. For production with funding, we could add GPT-4 as a premium tier for complex queries.

---

### PRODUCT/IMPACT QUESTIONS

**Q9: What's your target market and go-to-market strategy?**

> Primary: Special education coordinators and CBSE/ICSE schools in India with inclusive classrooms. Secondary: EdTech platforms (BYJU's, Unacademy) as a white-label adaptive layer. Go-to-market: pilot with 2-3 schools in Tier 1 cities, gather learning outcome data, then approach state government SSA (Sarva Shiksha Abhiyan) programs which mandate inclusive education.

---

**Q10: How do you measure if this actually improves learning outcomes?**

> The quiz submission system (`POST /quiz/submit`) logs every student's score per chapter. Teachers can see this on the dashboard. We can A/B compare: same chapter, control group uses normal textbook, test group uses EUREKA — measure quiz scores, time-on-task, and re-attempt rates. The feedback loop also lets students rate content quality which feeds back into retrieval weighting.

---

**Q11: Can't a teacher just use ChatGPT to do this?**

> ChatGPT lacks four things we have: (1) **Curriculum alignment** — we're chapter/grade/subject specific, not general. (2) **PDF grounding** — teacher's own materials become the source. (3) **Profile-specific UI** — the ADHD checkpoint flow, dyslexia fonts, hearing impairment visual contexts are purpose-built, not a chat interface. (4) **Progress tracking** — quiz scores, flashcard performance, teacher dashboard. EUREKA is a system, not a prompt.

---

**Q12: What about students without internet access?**

> The FAISS index and embeddings run fully locally. We could package EUREKA as an offline-capable Electron/PWA app where the LLM runs via Ollama locally. The architecture already supports this — swap Groq for Ollama in `config.py` and the system runs 100% offline. This is a direct roadmap item for rural school deployment.

---

**Q13: How is this different from existing tools like Microsoft Immersive Reader?**

> Immersive Reader does text formatting (fonts, spacing, read-aloud). EUREKA does **content transformation** — it doesn't just reformat, it restructures the pedagogy. For ADHD, it breaks the chapter into chunks with embedded quizzes. For visual impairment, it generates audio descriptions of diagrams. For dyslexia, it rewrites at a lower reading level with simpler vocabulary. These are fundamentally different operations.

---

**Q14: What are the limitations of your current system?**

> Honest answer: (1) LLM outputs vary — same prompt can give slightly different structure each time. (2) No image understanding — if a chapter has diagrams, we describe them textually but can't actually process the image from the PDF yet (roadmap: add vision model). (3) Auth is prototype-grade. (4) No real-time collaboration or teacher-student messaging. (5) Quiz questions are LLM-generated — quality control via teacher review is not yet built.

---

**Q15: If you had 6 more months, what would you build?**

> (1) Vision model integration to actually read and describe PDF diagrams. (2) Voice input — students with motor disabilities can ask questions verbally. (3) Parent dashboard with weekly progress reports. (4) Offline mode via Ollama. (5) Regional language support (Hindi, Tamil, Telugu adaptation). (6) Adaptive difficulty — if a student scores <60% on a quiz, the next attempt adds more checkpoints and simpler language automatically.

---

**Q16: Google's NotebookLM also lets you upload PDFs and ask questions about them. How are you different — and better?**

> Great question — NotebookLM is a strong product, but it is built for a completely different use case. Here's the direct comparison:

| | **NotebookLM** | **EUREKA** |
|---|---|---|
| **Purpose** | General-purpose document Q&A | Disability-specific content adaptation |
| **Output** | Chat answers, podcast summaries | Structured learning experiences per disability profile |
| **ADHD support** | None | Chunk + checkpoint flow, spaced repetition, inline MCQs |
| **Dyslexia support** | None | Simplified vocabulary, Grade 6 reading level rewrite |
| **Visual impairment** | None | Audio descriptions of diagrams + TTS script |
| **Hearing impairment** | None | Visual context + simplified text |
| **Cognitive disability** | None | Simplified + audio script |
| **Curriculum alignment** | Generic — any document | NCERT chapter/grade/subject filtered RAG |
| **Progress tracking** | None | Quiz scores, teacher dashboard, feedback loop |
| **Interactive checkpoints** | None | Section-by-section unlock with MCQ gates |
| **Offline capability** | No (Google cloud only) | Designed for local FAISS + Ollama swap |
| **Target user** | Researchers, professionals, general users | Students with special needs, teachers, schools |
| **Cost for schools** | Requires Google account, cloud dependency | Fully open-source, self-hostable, zero API cost |

> **The fundamental difference:** NotebookLM asks *"what does this document say?"* EUREKA asks *"how do I teach this document to a student with ADHD?"* — those are completely different problems. NotebookLM is a knowledge retrieval tool. EUREKA is a pedagogical transformation engine. We're not competing for the same user or use case — but if a judge asks, we win on inclusivity, curriculum specificity, interactivity, and the fact that NotebookLM has zero accessibility features for disabled learners.

---

## 9. ONE-LINER SUMMARY FOR THE PITCH

> *"EUREKA is an AI tutoring system that reads any textbook chapter and instantly transforms it into a personalised learning experience for students with ADHD, dyslexia, visual, hearing, or cognitive disabilities — using RAG-powered LLMs, profile-specific prompts, and interactive checkpoints that keep students engaged while ensuring they actually learn."*

---
