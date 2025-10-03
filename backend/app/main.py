
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import rag, health


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


