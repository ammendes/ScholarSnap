import feedparser
import httpx
from datetime import datetime, timedelta
from app.config import ARXIV_API_URL, DEFAULT_DAYS, BATCH_SIZE

# Async function to fetch recent arXiv papers
async def fetch_recent_arxiv_papers(topic: str, days: int = DEFAULT_DAYS, batch_size: int = BATCH_SIZE):
    params = {
        "search_query": f"all:\"{topic}\"",  # Use phrase search for stricter matching
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
    
    # Filter papers by publication date and topic phrase
    cutoff = datetime.utcnow() - timedelta(days=days)
    topic_lower = topic.lower()
    papers = []
    for entry in feed.entries:
        published = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
        if published < cutoff:
            break
        authors = [author.name for author in entry.authors] if hasattr(entry, "authors") else []
        title_lower = entry.title.lower()
        abstract_lower = entry.summary.lower()
        # Only include papers where the full topic phrase appears in title or abstract
        if topic_lower in title_lower or topic_lower in abstract_lower:
            papers.append({
                "id": entry.id,
                "title": entry.title,
                "abstract": entry.summary,
                "published": entry.published,
                "authors": authors
            })
    return papers