from fastapi import FastAPI
from src.utils.db import Base, engine
from src.user.router import user_routes
from src.rag.router import rag_routes
from src.rag.models import DocumentModel
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "RAG System",
        "description": "Upload documents and ask questions using LangChain and Gemini.",
    },
]


app = FastAPI(
    title="AI RAG Backend API",
    description="A production-grade Python backend featuring JWT Authentication and AI Document Analysis via LangChain.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes)
app.include_router(rag_routes)