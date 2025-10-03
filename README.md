# ScholarSnap

AI-powered research assistant that surfaces the *latest* research papers (e.g. from arXiv) for a topic and produces concise, structured summaries using a Retrieval-Augmented Generation (RAG) pipeline backed by a **local LLM via Ollama**.

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

## Current Status (Phase 1–5 Complete)
✅ Minimalistic chat UI: centered prompt, wide input bar, send button enabled only when text is entered.
✅ Backend scaffold (FastAPI) with health check and `/rag/summary` endpoint.
✅ Frontend and backend are integrated: chat input sends topic to backend and displays response.
✅ Real arXiv retrieval: backend fetches recent papers matching topic, filters by date, and returns metadata (title, abstract, authors).
✅ LLM integration: backend sends context to local Ollama server and returns generated summary.
✅ Modular backend architecture: separated services and routers for maintainability.
✅ Configuration management: centralized config loading from YAML file.
✅ CORS middleware: enables frontend-backend communication across different ports.
🚧 Next: Add vector embeddings, persistent storage, and background refresh jobs.

## High-Level Architecture (Target State)
```
┌──────────┐      Query/topic       ┌──────────────────────┐
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
			main.py              # FastAPI entrypoint, router registration
			config.py            # Configuration loader from YAML
			routers/
				health.py        # Health check endpoint
				rag.py           # RAG summary endpoint
			services/
				arxiv.py         # Real arXiv API integration
				llm.py           # Ollama LLM integration & context building
		config.yaml              # Application configuration
		requirements.txt
	README.md
	LICENSE
	.gitignore
```

## Backend API (Current)
`GET /health/` → `{ "status": "ok" }`

`GET /rag/summary?topic=fourier` 
Response:
```json
{
	"topic": "fourier",
	"summary": "• Paper title 1\n• Paper title 2\n• Paper title 3",
	"papers": [
		{
			"id": "http://arxiv.org/abs/2410.xxxxx",
			"title": "Recent Advances in Fourier Analysis",
			"abstract": "This paper presents...",
			"published": "2024-10-02T17:30:15Z",
			"authors": ["Author Name", "Co-Author Name"]
		}
	]
}
```

### Planned Enhancements
- Add `source_url`, `authors`, `categories` fields.
- Add `embedding_model`, `llm_model` metadata.
- Add `/rag/raw` to return full retrieved context.

## Ollama Integration (Complete)
✅ Ollama integration implemented with configurable model selection.
✅ Configuration via `config.yaml`:
```yaml
ollama:
  url: "http://localhost:11434/api/generate"
  model: "mistral:latest"
  
arxiv:
  api_url: "https://export.arxiv.org/api/query"
  default_days: 7
  batch_size: 5
```
✅ Implemented POST to Ollama API with structured prompts for paper title extraction.
✅ Streaming response handling and JSON parsing from Ollama server.

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
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```
Open: http://localhost:8002/docs

Note: Ensure Ollama is running locally with a model pulled (e.g., `ollama pull mistral`).

### Testing (Future)
- Will add pytest + httpx async client tests under `backend/tests/`.
- Frontend: Vitest + React Testing Library planned.

## Next Actions (Implementation Backlog)
Short-Term:
1. ✅ ~~Implement real arXiv client (httpx, query building, date filter).~~
2. ✅ ~~Add basic error handling + timeouts.~~
3. ✅ ~~Implement Ollama summarizer (stream or full response).~~
4. Add vector embeddings with sentence-transformers for semantic search.
5. Introduce dedupe key (paper id) in vector store.
6. Add pydantic models for Paper / Summary for better type safety.

Medium:
7. Replace in-memory processing with FAISS persistent index.
8. Add `/config` endpoint exposing current models.
9. Implement proper error handling and user feedback for LLM failures.
10. Add content filtering and quality checks for paper summaries.

Longer-Term:
11. Topic subscriptions & background refresh.
12. Summarization evaluation harness.
13. Multi-model ensemble or reranking (e.g., Cohere Rerank optional).
14. Deploy docker-compose for full stack.

## Design Decisions (Rationale Log)
| Decision | Rationale | Revisit When |
|----------|-----------|--------------|
| React+Tailwind over Streamlit | Better engineering signaling, modular growth | If rapid internal demo needed |
| FastAPI | Async HTTP, ecosystem, OpenAPI docs | Only if heavy streaming or gRPC needed |
| In-memory store first | Speed of iteration | When persistence or scale required |
| Hash embeddings placeholder | Avoid early dependency weight | After arXiv integration stable |
| Local Ollama LLM | Privacy + offline dev | If quality insufficient / need hosted API |

## Environment Variables (Current Configuration)
Configuration is now managed via `config.yaml`:
```yaml
ollama:
  url: "http://localhost:11434/api/generate"
  model: "mistral:latest"
  
arxiv:
  api_url: "https://export.arxiv.org/api/query"
  default_days: 7
  batch_size: 5
```

Planned environment variable overrides:
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
