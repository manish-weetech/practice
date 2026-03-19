from sqlalchemy import Boolean, Column, Integer, String, Enum
import enum
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    items = relationship("Item", back_populates="owner")
