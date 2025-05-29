import enum
import uuid

from db.base import Base

# from sqlalchemy import Enum
# from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    MANAGER = "manager"


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNDISCLOSED = "undisclosed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))

    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    full_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    age = Column(Integer, unique=True)
    # gender = Column(SqlEnum(Gender), default=Gender.UNDISCLOSED)

    # role = Column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)
    gender = Column(String, default="undisclosed")
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}>"
