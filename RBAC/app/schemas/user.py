from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

# Properties to receive via API on creation
class UserSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.USER

# Properties to receive via API on update
class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

# Properties to return via API
class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
