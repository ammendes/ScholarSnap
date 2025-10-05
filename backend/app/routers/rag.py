from fastapi import APIRouter, Query
from app.services.arxiv import fetch_recent_arxiv_papers
from app.services.llm import build_context
from app.services.llm import get_paper_list
from app.config import DEFAULT_DAYS

router = APIRouter()

#  RAG/summary endpoint
@router.get("/rag/summary")
async def rag_summary(topic: str = Query(...)):
    papers = await fetch_recent_arxiv_papers(topic, days=DEFAULT_DAYS)
    context = build_context(papers)
    #print("\n--- CONTEXT SENT TO LLM ---\n", context, "\n--- END CONTEXT ---\n")
    summary = await get_paper_list(topic, context)
    return {
        "topic": topic,
        "summary": summary,
        "papers": papers,
    }