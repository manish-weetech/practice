from fastapi import HTTPException, status
from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.services import UserService
import logging

logger = logging.getLogger(__name__)

# Single instance of the UserService providing DI injection capabilities into the controller
user_service = UserService()

def register(body: UserSchema, db: Session):
    try:
        new_user = user_service.create_user(body, db)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while registering.")

def login_user(body: LoginSchema, db: Session):
    try:
        token = user_service.authenticate_user(body, db)
        return {"token": token}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        logger.error(f"Error logging in user: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during login.")