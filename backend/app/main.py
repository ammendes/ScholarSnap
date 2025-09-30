from fastapi import FastAPI, Query
import feedparser
import httpx
from datetime import datetime, timedelta
import yaml
import json


# Open and read configuration from config.yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)

OLLAMA_API_URL = config["ollama"]["url"]
OLLAMA_MODEL = config["ollama"]["model"]
ARXIV_API_URL = config["arxiv"]["api_url"]
DEFAULT_DAYS = config["arxiv"]["default_days"]
BATCH_SIZE = config["arxiv"]["batch_size"]


async def call_ollama_llm(topic: str, context: str):
    # Prompt tags explanation:
    # SYSTEM: Sets the LLM's role or behavior (e.g., scientific assistant)
    # USER: The user's request or question
    # CONTEXT: Background info or retrieved documents (papers)
    # OUTPUT: Specifies the desired format or style of the answer

    # Send full context, but instruct LLM to output only the paper titles as a bullet list
    prompt = (
        "Below is a list of research papers, each with title, authors, and abstract.\n"
        "Your task: Output only the paper titles as a bullet list. Do not include authors or abstracts.\n\n"
        f"{context}"
    )
    payload = {"model": OLLAMA_MODEL, "prompt": prompt}
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(OLLAMA_API_URL, json=payload)
        # Ollama streams JSON objects, one per line
        summary = ""
        #print("\n--- RAW LLM RESPONSE ---")
        for line in response.iter_lines():
            if line:
                #print(line)
                obj = json.loads(line)
                summary += obj.get("response", "")
        #print("--- END RAW LLM RESPONSE ---\n")
        return summary or "No summary generated."


def build_context(papers):
    context = ""
    for paper in papers:
        context += (
            f"Title: {paper['title']}\n"
            f"Authors: {', '.join(paper['authors'])}\n"
            f"Abstract: {paper['abstract']}\n\n"
        )
    return context


# Initialize FastAPI app
app = FastAPI()


# Async function to fetch recent arXiv papers
async def fetch_recent_arxiv_papers(topic: str, days: int = DEFAULT_DAYS, batch_size: int = BATCH_SIZE):
    params = {
        "search_query": f"all:{topic}",
        "start": 0,
        "max_results": batch_size,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    # Fetch and parse the RSS feed
    async with httpx.AsyncClient() as client:
        response = await client.get(ARXIV_API_URL, params=params)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
    
    # Filter papers by publication date
    cutoff = datetime.utcnow() - timedelta(days=days)
    papers = []
    for entry in feed.entries:
        published = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
        if published < cutoff:
            break
        authors = [author.name for author in entry.authors] if hasattr(entry, "authors") else []
        papers.append({
            "id": entry.id,
            "title": entry.title,
            "abstract": entry.summary,
            "published": entry.published,
            "authors": authors
        })
    return papers


# Health check endpoint
@app.get("/health/")
async def health():
    return {"status": "ok"}


# Mock RAG summary endpoint
@app.get("/rag/summary")
async def rag_summary(topic: str = Query(...)):
    papers = await fetch_recent_arxiv_papers(topic, days=DEFAULT_DAYS)
    context = build_context(papers)
    print("\n--- CONTEXT SENT TO LLM ---\n", context, "\n--- END CONTEXT ---\n")
    summary = await call_ollama_llm(topic, context)
    return {
        "topic": topic,
        "summary": summary,
        "papers": papers,
    }
