from typing import Optional
from pydantic import BaseModel

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
