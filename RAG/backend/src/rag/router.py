from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from src.user.models import UserModel
from src.utils.helpers import is_authentication
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.rag.dtos import AskRequest, AskResponse, UploadResponse, DocumentResponseSchema
from typing import List
from src.rag import controller

rag_routes = APIRouter(prefix="/rag", tags=["RAG System"])

@rag_routes.post(
    "/upload", 
    response_model=UploadResponse, 
    status_code=status.HTTP_200_OK,
    summary="Upload a knowledge document",
    description="Accepts a highly complex PDF or DOCX file, chunks the semantics, embeds them using Google AI, and stores the vectors securely in ChromaDB for similarity queries."
)
async def upload_document(
    file: UploadFile = File(...),
    display_name: str = Form(...),
    user: UserModel = Depends(is_authentication),
    db: Session = Depends(get_db)
):
    """Parses and stores the newly uploaded document."""
    return await controller.upload_document(file, db, user.id, display_name)


@rag_routes.post(
    "/ask", 
    response_model=AskResponse, 
    status_code=status.HTTP_200_OK,
    summary="Ask a question against document history",
    description="Takes a natural language question constraint, performs a mathematically rigorous similarity search across isolated vector chunks, and synthesizes an incredibly accurate LLM response."
)
def ask_question(
    body: AskRequest,
    user: UserModel = Depends(is_authentication)
):
    """Asks a question regarding the previously uploaded documents."""
    return controller.ask_question(body)

@rag_routes.get(
    "/documents", 
    response_model=List[DocumentResponseSchema], 
    status_code=status.HTTP_200_OK,
    summary="Get user document history",
    description="Returns all parsed documents linked to the authenticated user."
)
def get_user_documents(
    user: UserModel = Depends(is_authentication),
    db: Session = Depends(get_db)
):
    """Returns all documents processed by the current user."""
    return controller.get_user_documents(db, user.id)
