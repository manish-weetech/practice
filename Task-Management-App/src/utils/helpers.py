from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.utils.settings import settings
from src.user.models import UserModel
from src.utils.db import get_db
from src.utils.exceptions import UnauthorizedException
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError

# Password Hashing
password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

# JWT Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    try:
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = data.get("_id")
        
        if not user_id:
            raise UnauthorizedException("Invalid token payload")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise UnauthorizedException("User not found")

        return user
    except InvalidTokenError:
        raise UnauthorizedException("Invalid or expired token")
