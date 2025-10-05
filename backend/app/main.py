

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers import rag, health
from app.langgraph_workflow import langgraph_app, ChatState


# Initialize FastAPI app and include routers
app = FastAPI()
app.include_router(rag.router)
app.include_router(health.router)


# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LangGraph-powered conversational endpoint
@app.post("/chat/")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("message")
    state = {
        "user_input": user_input,
        "topic": None,
        "confirmed": False,
        "papers": None,
        "summary": None,
        "clarification": None,
    }
    # Run the workflow (async)
    result = await langgraph_app.ainvoke(state)
    return result


