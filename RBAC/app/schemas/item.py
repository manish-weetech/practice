from typing import Optional
from pydantic import BaseModel

# Properties to receive on item creation
class ItemSchema(BaseModel):
    title: str
    description: Optional[str] = None

# Properties to receive on item update
class ItemUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# Properties to return to client
class ItemResponseSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner_id: int

    class Config:
        from_attributes = True
