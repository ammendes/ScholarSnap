
from langchain_ollama import OllamaLLM
import httpx
import json
from app.config import OLLAMA_API_URL, OLLAMA_MODEL


# Async function to validate topic with Ollama LLM
async def validate_topic_with_llm(topic: str):
    llm = OllamaLLM(model=OLLAMA_MODEL)
    prompt = (
        "You are a scientific assistant. "
        "Your task is to determine if the given topic is a valid scientific research topic. "
        "Anatomical, medical, biological, physical, chemical, computational, and engineering topics are all valid. "
        "When checking if a topic is valid, ignore capitalization/case. "
        "If the topic is valid, reply ONLY with: 'Valid' "
        "If the topic is invalid, reply ONLY with: 'Invalid scientific topic. Please try a different one.' "
        f"\nTopic: {topic}"
    )
    result = await llm.ainvoke(prompt)
    return result.strip()


# Async function to process and get paper list summary from Ollama LLM
async def get_paper_list(topic: str, context: str):

    # Only include paper title in the prompt, and instruct LLM to output only bulletpoints
    if not context.strip():
        return "No papers found for this topic."
    prompt = (
        f"Below is a list of research paper titles.\n"
        f"Your task: Output ONLY the paper titles provided below as a list of bulletpoints.\n"
        f"Use the dot character (•) as the bullet.\n"
        f"Do NOT include authors, abstracts, summaries, explanations, or any other text.\n"
        f"Do NOT generate or invent titles. ONLY output the exact titles given, in the order they appear.\n"
        f"Start your response with: 'Here are the latest papers on '{topic}'':\n"
        f"The list of papers is as follows:\n"
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
        # Do NOT append processing prompt here; handled by backend separately
        return summary.strip() or "No summary generated."


# Helper function to build context from paper titles
def build_context(papers):
    context = ""
    for paper in papers:
        context += f"{paper['title']}\n"
    return context


# Async function to classify user's response to the processing prompt
async def classify_processing_response(user_response: str):
    llm = OllamaLLM(model=OLLAMA_MODEL)
    prompt = (
        "You are a scientific assistant. "
        "Classify the following user response as one of three categories: 'positive', 'negative', or 'unclear'. "
        "A positive response means the user wants to proceed with processing. "
        "A negative response means the user does NOT want to proceed. "
        "If the response is ambiguous or you cannot tell, reply ONLY with 'I could not understand that. Please be more specific. (yes/no)'. "
        "Reply ONLY with one word: 'positive', 'negative', or 'unclear'. "
        f"\nUser response: {user_response}"
    )
    result = await llm.ainvoke(prompt)
    return result.strip().lower()