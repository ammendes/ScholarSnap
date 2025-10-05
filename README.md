
# ScholarSnap

ScholarSnap is an AI-powered research assistant that surfaces the latest research papers from arXiv for a given topic and produces concise, structured summaries using a Retrieval-Augmented Generation (RAG) pipeline backed by a local LLM (Ollama/Mistral).

## Features & Current State

- **LangGraph workflow**: Conversational orchestration with greeting, topic validation, RAG pipeline, and clarification/error handling.
- **Strict topic validation**: LLM checks if the topic is a valid scientific research topic (including anatomical/medical terms) and prompts for re-entry if invalid.
- **Phrase-based arXiv search**: Only returns papers where the full topic phrase appears in the title or abstract, ensuring high relevance.
- **LLM summarization**: Only paper titles are sent to the LLM, which outputs a bullet-point list. No summaries, explanations, or extra text.
- **Frontend chat UI**: Minimal React app with clear error and clarification handling, showing bot and user messages in a chat layout.
- **Ollama integration**: Uses local Mistral model by default, configurable via YAML.
- **Modular codebase**: FastAPI backend with routers/services, React frontend, and centralized config.

## Repository Structure
```
ScholarSnap/
	frontend/                # React + Vite + Tailwind
		src/
			App.tsx              # Chat UI
			main.tsx
			index.css
		package.json
		tsconfig.json
		tailwind.config.js
	backend/
		app/
			main.py              # FastAPI entrypoint, router registration
			config.py            # Configuration loader from YAML
			langgraph_workflow.py# LangGraph workflow orchestration
			routers/
				health.py          # Health check endpoint
				rag.py             # RAG summary endpoint
			services/
				arxiv.py           # arXiv API integration (phrase search)
				llm.py             # Ollama LLM integration & context building
		config.yaml            # Application configuration
		requirements.txt
	README.md
	LICENSE
	.gitignore
```

## Backend API

`POST /chat/` (main conversational endpoint)
Request:
```json
{ "message": "fourier" }
```
Response (valid topic, papers found):
```json
{
	"greeting": "Hello! What scientific topic are you interested in today?",
	"topic": "fourier",
	"summary": "• Paper title 1\n• Paper title 2\n• Paper title 3",
	"papers": [
		{ "id": "http://arxiv.org/abs/2410.xxxxx", "title": "Recent Advances in Fourier Analysis", "abstract": "...", "published": "2024-10-02T17:30:15Z", "authors": ["Author Name"] }
	],
	"paper_list": "- Recent Advances in Fourier Analysis (Authors: Author Name)",
	"no_papers": null
}
```
Response (valid topic, no papers found):
```json
{
	"greeting": "Hello! What scientific topic are you interested in today?",
	"topic": "anal fissure",
	"summary": "No papers found for this topic.",
	"papers": [],
	"paper_list": null,
	"no_papers": "No papers found for this topic."
}
```
Response (invalid topic):
```json
{
	"greeting": "Hello! What scientific topic are you interested in today?",
	"topic": null,
	"summary": null,
	"papers": null,
	"paper_list": null,
	"no_papers": null,
	"clarification": "Invalid scientific topic. Please try a different one."
}
```

## Configuration

Configuration is managed via `config.yaml`:
```yaml
ollama:
	url: "http://localhost:11434/api/generate"
	model: "mistral:latest"
arxiv:
	api_url: "https://export.arxiv.org/api/query"
	default_days: 7
	batch_size: 5
```

## Installation & Dev Workflow

### Prereqs
- Node 18+ / pnpm or npm
- Python 3.11+
- Ollama installed locally (with model pulled, e.g. `ollama pull mistral`)

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
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```
Open: http://localhost:8002/docs

## License
MIT

---
ScholarSnap is maintained as a demonstration of applied RAG with local inference. Iterative improvements are ongoing.
