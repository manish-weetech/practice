from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.token import TokenResponseSchema
from app.schemas.user import LoginSchema, UserResponseSchema, UserSchema
from app.models.user import UserRole
from app.crud.crud_user import user as crud_user

router = APIRouter()

@router.post("/login", response_model=TokenResponseSchema)
def login(
    form_data: LoginSchema,
    db: Session = Depends(deps.get_db),
) -> Any:
    user = crud_user.authenticate(
        db, email=form_data.email, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserResponseSchema)
def register(
    user_in: UserSchema,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create new user.
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    # Force role to USER for public registration
    user_in.role = UserRole.USER
    return crud_user.create(db, obj_in=user_in)
