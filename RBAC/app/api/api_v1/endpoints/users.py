from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.crud_user import user as crud_user
from app.schemas.user import UserResponseSchema, UserSchema
from app.models.user import UserRole

router = APIRouter()

@router.get("/", response_model=List[UserResponseSchema], dependencies=[Depends(deps.RoleChecker([UserRole.ADMIN]))])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    users = db.query(crud_user.model if hasattr(crud_user, 'model') else crud_user.get_db_model()).offset(skip).limit(limit).all()
    # Wait, crud_user doesn't have .model here because I reverted CRUDBase.
    # I'll just use the User model directly or fix the logic.
    from app.models.user import User
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UserResponseSchema)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserSchema,
) -> Any:
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    return crud_user.create(db, obj_in=user_in)

@router.get("/me", response_model=UserResponseSchema)
def read_user_me(
    current_user: UserResponseSchema = Depends(deps.get_current_active_user),
) -> Any:
    return current_user
