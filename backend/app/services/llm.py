import httpx
import json
from app.config import OLLAMA_API_URL, OLLAMA_MODEL


# Function to call Ollama LLM API
async def call_ollama_llm(topic: str, context: str):
    # Prompt tags explanation:
    # SYSTEM: Sets the LLM's role or behavior (e.g., scientific assistant)
    # USER: The user's request or question
    # CONTEXT: Background info or retrieved documents (papers)
    # OUTPUT: Specifies the desired format or style of the answer

    # Send full context, but instruct LLM to output only the paper titles as a bullet list
    prompt = (
        "Below is a list of research papers, each with title, authors, and abstract.\n"
        "Your task: Output only the paper titles as a list of bulletpoints, using the dot character (•) as the bullet. Do not include authors or abstracts.\n\n"
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