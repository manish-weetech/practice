from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.utils.settings import settings
from src.user.models import UserModel
from src.utils.db import get_db
import jwt
from jwt.exceptions import InvalidTokenError

security = HTTPBearer()

def is_authentication(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials

        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = data.get("_id")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are unauthorized",
            )

        return user
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized",
        )
