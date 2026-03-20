from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta
import jwt
from src.user.dtos import UserSchema, LoginSchema

password_hash = PasswordHash.recommended()

class UserService:
    """Handles the core business logic, hashing, and database operations for Users."""
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return password_hash.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return password_hash.verify(password, hashed_password)

    def create_user(self, body: UserSchema, db: Session) -> UserModel:
        is_username = db.query(UserModel).filter(UserModel.username == body.username).first()
        if is_username:
            raise ValueError("Username already exists")
            
        is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
        if is_email:
            raise ValueError("Email already exists")

        hashed_pwd = self.get_password_hash(body.password)
        new_user = UserModel(
            name=body.name,
            username=body.username,
            hash_password=hashed_pwd,
            email=body.email,
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def authenticate_user(self, body: LoginSchema, db: Session) -> str:
        user = db.query(UserModel).filter(UserModel.email == body.email).first()
        if not user or not self.verify_password(body.password, user.hash_password):
            raise PermissionError("You entered wrong email and password")

        exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
        token = jwt.encode(
            {"_id": user.id, "exp": exp_time.timestamp()},
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
        return token
