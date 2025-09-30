# ScholarSnap

AI-powered research assistant that surfaces the *latest* research papers (e.g. from arXiv) for a topic and produces concise, structured summaries using a Retrieval-Augmented Generation (RAG) pipeline backed by a **local LLM via Ollama**.

## Why This Exists
Researchers, engineers, and candidates preparing for interviews need a fast snapshot of what changed recently in their domain ("What’s new in diffusion models this week?"). ScholarSnap automates that: fetch → embed → retrieve → summarize.

## Development Phases (Roadmap)
1. Frontend First (React + Tailwind) – wire to mocked backend responses for fast UI iteration.
2. Core Backend Skeleton (FastAPI) – health + RAG placeholder (mock data + fake embeddings + placeholder summarizer).
3. Real arXiv Integration – implement query + pagination + filtering by date window.
4. Embeddings Upgrade – swap hash placeholder for real model (sentence-transformers or local embedding model via Ollama / HF Inference).
5. Local LLM Summarization – call Ollama (e.g. `mistral`, `llama3`, etc.) with a structured prompt.
6. Vector Store Upgrade – introduce FAISS (persistent) with refresh policy & dedupe.
7. Background Refresh Job – periodic ingestion for subscribed topics.
8. Evaluation / Prompt Refinement – add lightweight eval script + prompt versions.
9. Optional: Auth, saved topics, deployment (Docker / Fly.io / Render).

## Current Status (Phase 1–2 Skeleton)
✅ Frontend scaffold (React + Vite + Tailwind).
✅ Minimalistic chat UI: centered prompt, wide input bar, send button enabled only when text is entered.
✅ Backend scaffold (FastAPI) with placeholder RAG `/rag/summary` endpoint.  
✅ In-memory mock vector store + hash-based embeddings (deterministic placeholder).  
🚧 Next: Replace mock arXiv client with real API calls.  

## High-Level Architecture (Target State)
```
┌──────────┐      Query/topic        ┌─────────────────────┐
│  React   │ ─────────────────────▶ │  FastAPI Backend     │
│ Frontend │                        │  /rag/summary        │
└────┬─────┘                        ├──────────┬───────────┤
	 │ Summary JSON                 │          │           │
	 ▼                              ▼          ▼           ▼
 UI Rendering                ArXiv Client  Vector Store  LLM (Ollama)
									▲          │           ▲
									└──── Embedder ◀───────┘
```

### Components (Planned)
- Frontend: React (Vite) + Tailwind; later could add routing + caching + skeleton loaders.
- Backend: FastAPI (modular routers, pydantic schemas, async httpx for arXiv).
- Embeddings: Initially hash placeholder → `sentence-transformers` (e.g. `all-MiniLM-L6-v2`) or local embedding model.
- Vector Store: Start in-memory → FAISS (disk persistence) → optional Chroma/Weaviate if needed.
- LLM: Local Ollama model (default `mistral`) with fallback to others via env config.
- Scheduler: (Later) APScheduler or simple asyncio background task for refresh.

## Repository Structure
```
ScholarSnap/
	frontend/                # React + Vite + Tailwind
		src/
			App.tsx
			main.tsx
			index.css
		package.json
		tsconfig.json
		tailwind.config.js
	backend/
		app/
			main.py              # FastAPI entrypoint
			routers/
				health.py
				rag.py             # RAG summary endpoint (placeholder)
			rag/
				arxiv_client.py    # Mock now → real arXiv queries later
				embeddings.py       # Placeholder embedding logic
				vector_store.py     # Simple in-memory store
				llm.py              # Placeholder Ollama wrapper
				pipeline.py         # Orchestration
		requirements.txt
	README.md
	LICENSE
	.gitignore
```

## Backend API (Current)
`GET /health/` → `{ "status": "ok" }`

`GET /rag/summary?topic=diffusion+models&days=7&k=5`
Response (placeholder):
```json
{
	"topic": "diffusion models",
	"summary": "Summary for diffusion models ...",
	"papers": [ {"id": "mock:0", "title": "Diffusion Models Paper 0", ...} ]
}
```

### Planned Enhancements
- Add `source_url`, `authors`, `categories` fields.
- Add `embedding_model`, `llm_model` metadata.
- Add `/rag/raw` to return full retrieved context.

## Ollama Integration Plan
1. Install Ollama (https://ollama.ai) and pull a model: `ollama pull mistral`.
2. Add environment variable: `OLLAMA_MODEL=mistral` (fallback default).
3. Implement POST to `http://localhost:11434/api/generate` with prompt template:
	 ```
	 SYSTEM: You are a scientific research assistant. Summarize new findings.
	 USER: Summarize the latest research in <topic>. Use bullet points.
	 CONTEXT:
	 <paper 1 title> - <abstract>
	 ...
	 OUTPUT: Concise bullet list + optional key trends.
	 ```
4. Stream tokens to client (optional improvement).

## Prompting Strategy (Draft)
Goal: Balanced brevity + signal of novelty.
Sections:
1. One-line high-level shift.
2. 3–7 bullet insights (each referencing a paper ID or short title handle).
3. Emerging directions (optional if detectable).

## Installation & Dev Workflow

### Prereqs
- Node 18+ / pnpm or npm
- Python 3.11+
- (Later) Ollama installed locally

### Frontend Dev
```
cd frontend
npm install
npm run dev
```
Opens: http://localhost:5173

### Backend Dev
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Open: http://localhost:8000/docs

### Testing (Future)
- Will add pytest + httpx async client tests under `backend/tests/`.
- Frontend: Vitest + React Testing Library planned.

## Next Actions (Implementation Backlog)
Short-Term:
1. Implement real arXiv client (httpx, query building, date filter).
2. Introduce dedupe key (paper id) in vector store.
3. Add pydantic models for Paper / Summary.
4. Add basic error handling + timeouts.

Medium:
5. Swap embeddings to sentence-transformers (configurable embedding batch size).
6. Implement Ollama summarizer (stream or full response).
7. Replace in-memory store with FAISS persistent index.
8. Add `/config` endpoint exposing current models.

Longer-Term:
9. Topic subscriptions & background refresh.
10. Summarization evaluation harness.
11. Multi-model ensemble or reranking (e.g., Cohere Rerank optional).
12. Deploy docker-compose for full stack.

## Design Decisions (Rationale Log)
| Decision | Rationale | Revisit When |
|----------|-----------|--------------|
| React+Tailwind over Streamlit | Better engineering signaling, modular growth | If rapid internal demo needed |
| FastAPI | Async HTTP, ecosystem, OpenAPI docs | Only if heavy streaming or gRPC needed |
| In-memory store first | Speed of iteration | When persistence or scale required |
| Hash embeddings placeholder | Avoid early dependency weight | After arXiv integration stable |
| Local Ollama LLM | Privacy + offline dev | If quality insufficient / need hosted API |

## Environment Variables (Planned)
```
OLLAMA_MODEL=mistral
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
ARXIV_MAX_RESULTS=200
VECTOR_STORE_PATH=.data/index
```

## Contributing (Future)
- Add pre-commit config (black, isort, ruff / flake8).
- Add lint script for frontend.

## License
MIT

---
Maintained as a portfolio-quality demonstration of applied RAG with local inference. Iteratively harden rather than over-engineer prematurely.
