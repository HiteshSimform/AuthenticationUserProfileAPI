from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from enum import Enum
import re


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    undisclosed = "undisclosed"


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"
    manager = "manager"


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    hashed_password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    bio: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = Gender.undisclosed
    role: Optional[UserRole] = UserRole.user

    @field_validator("hashed_password")
    def validate_password(cls, password: str):
        if not all(
            re.search(pattern, password)
            for pattern in [r"[A-Z]", r"[a-z]", r"[0-9]", r"[\W_]"]
        ):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
            )
        return password

    @field_validator("username")
    def validate_username(cls, username: str):
        if not re.match(r"[a-zA-Z0-9_]+$", username):
            raise ValueError(
                "Username must contain alphanumeric characters or underscores."
            )
        return username

    def get_gender_value(self):
        return self.gender.value


class UserLogin(BaseModel):
    username: str
    password: str

    @field_validator("password")
    def validate_password_length(cls, password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return password


class UserUpdate(BaseModel):
    full_name: Optional[str]
    bio: Optional[str]
    age: Optional[int]
    gender: Optional[Gender]
    hashed_password: Optional[str] = Field(None, min_length=8)

    @field_validator("hashed_password")
    def validate_password(cls, password: Optional[str]):
        if password and len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return password


class UserOut(BaseModel):
    public_id: str
    username: str
    email: EmailStr
    full_name: Optional[str]
    bio: Optional[str]
    age: Optional[int]
    gender: Gender
    role: UserRole
    is_active: bool

    class Config:
        orm_mode = True
