from fastapi import UploadFile, HTTPException, status
from src.rag.dtos import AskRequest, AskResponse, UploadResponse, DocumentResponseSchema, ChatHistoryResponseSchema
from src.rag.services import RagService
from src.rag.models import DocumentModel, ChatHistoryModel
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

# Single instance of the RagService tracking ChromaDB globally
rag_service = RagService()

async def upload_document(file: UploadFile, db: Session, user_id: int, display_name: str = None):
    try:
        doc_id = await rag_service.process_document(file, db, user_id, display_name)
        return UploadResponse(doc_id=doc_id, filename=file.filename, display_name=display_name or file.filename, message="File processed and stored successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while processing the file.")

def ask_question(body: AskRequest, db: Session):
    try:
        if not body.question.strip():
            raise ValueError("Question cannot be empty.")
        answer = rag_service.answer_question(body.doc_id, body.question, db)
        return AskResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error asking question: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while answering the question.")

def get_user_documents(db: Session, user_id: int):
    docs = db.query(DocumentModel).filter(DocumentModel.user_id == user_id).order_by(DocumentModel.created_at.desc()).all()
    return docs

def get_chat_history(doc_id: str, db: Session):
    history = db.query(ChatHistoryModel).filter(ChatHistoryModel.doc_id == doc_id).order_by(ChatHistoryModel.created_at.asc()).all()
    return history
