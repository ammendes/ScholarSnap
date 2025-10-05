import httpx
import json
from app.config import OLLAMA_API_URL, OLLAMA_MODEL


# Function to call Ollama LLM API
async def get_paper_list(topic: str, context: str):

    # Send only paper titles, and instruct LLM to output only bulletpoints
    if not context.strip():
        return "No papers found for this topic."
    prompt = (
        f"Below is a list of research paper titles.\n"
        f"Your task: Output ONLY the paper titles as a list of bulletpoints, using the dot character (•) as the bullet. Do NOT include authors, abstracts, summaries, explanations, or any other text. Do not output anything except the bullet list.\n"
        f"Start your response with: Here are the latest papers on '{topic}':\n\n"
        f"{context}"
    )
    payload = {"model": OLLAMA_MODEL, "prompt": prompt}
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_API_URL, json=payload)
        # Ollama streams JSON objects, one per line
        summary = ""
        for line in response.iter_lines():
            if line:
                obj = json.loads(line)
                summary += obj.get("response", "")
        return summary or "No summary generated."


def build_context(papers):
    context = ""
    for paper in papers:
        context += f"{paper['title']}\n"
    return context