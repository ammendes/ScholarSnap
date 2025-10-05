

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
    # Track session state (could be improved with real session management)
    # For now, use a simple in-memory approach
    # You may want to use a persistent/session store for production
    if hasattr(app, "_last_state") and app._last_state.get("awaiting_processing_confirmation"):
        # The last state was awaiting confirmation, so treat input as response
        state = app._last_state.copy()
        state["user_response"] = user_input
    else:
        # New topic/session
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
    # Save state for next turn
    app._last_state = result.copy() if hasattr(result, "copy") else dict(result)
    return result


