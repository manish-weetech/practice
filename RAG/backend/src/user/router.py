from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema, UserResponseSchema, LoginSchema
from src.user import controller
from src.utils.helpers import is_authentication
from src.user.models import UserModel

user_routes = APIRouter(prefix="/user", tags=["Authentication"])


@user_routes.post(
    "/register", 
    response_model=UserResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="Creates a new user securely in the PostgreSQL database with an Argon2 hashed password."
)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register(body, db)


@user_routes.post(
    "/login", 
    status_code=status.HTTP_200_OK,
    summary="Login to obtain an access token",
    description="Authenticates the user's plain-text password against the hash and returns a valid JWT token for accessing protected routes."
)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)


@user_routes.get(
    "/is_auth", 
    response_model=UserResponseSchema, 
    status_code=status.HTTP_200_OK,
    summary="Get current user details",
    description="Validates the provided Bearer token and returns the database profile of the currently authenticated user."
)
def is_auth(user: UserModel = Depends(is_authentication)):
    return user
