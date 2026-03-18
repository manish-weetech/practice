from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.user.dtos import UserSchema, LoginSchema
from src.utils.exceptions import UnauthorizedException, BadRequestException
from src.utils.helpers import get_password_hash, verify_password
from src.utils.settings import settings
from datetime import datetime, timedelta
import jwt

class UserService:
    @staticmethod
    def register(db: Session, body: UserSchema):
        # Check if username or email already exists
        if db.query(UserModel).filter(UserModel.username == body.username).first():
            raise BadRequestException("Username already exists")
        
        if db.query(UserModel).filter(UserModel.email == body.email).first():
            raise BadRequestException("Email already exists")

        hash_password = get_password_hash(body.password)

        new_user = UserModel(
            name=body.name,
            username=body.username,
            hash_password=hash_password,
            email=body.email,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def login(db: Session, body: LoginSchema):
        user = db.query(UserModel).filter(UserModel.username == body.username).first()
        if not user or not verify_password(body.password, user.hash_password):
            raise UnauthorizedException("Invalid username or password")

        exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)

        token = jwt.encode(
            {"_id": user.id, "exp": exp_time.timestamp()},
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
        return {"token": token, "token_type": "bearer"}
