from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema, UserResponseSchema, LoginSchema
from src.user.service import UserService
from src.utils.helpers import get_current_user

user_routes = APIRouter(prefix="/user")

@user_routes.post(
    "/register", 
    response_model=UserResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return UserService.register(db, body)

@user_routes.post(
    "/login", 
    status_code=status.HTTP_200_OK,
    summary="User login with username and password"
)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    # Note: For strict OAuth2 compatibility, this should handle form data
    # but keeping LoginSchema for now as per project requirements
    return UserService.login(db, body)

@user_routes.get(
    "/me", 
    response_model=UserResponseSchema, 
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user info"
)
def get_me(current_user=Depends(get_current_user)):
    return current_user
