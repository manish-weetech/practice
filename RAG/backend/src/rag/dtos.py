from pydantic import BaseModel

class AskRequest(BaseModel):
    doc_id: str
    question: str

class AskResponse(BaseModel):
    answer: str

class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    display_name: str
    message: str

from datetime import datetime

class DocumentResponseSchema(BaseModel):
    id: int
    user_id: int
    doc_id: str
    filename: str
    display_name: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
