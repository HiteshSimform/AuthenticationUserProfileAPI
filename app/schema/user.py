from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


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
    username: str
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = Gender.undisclosed
    role: Optional[UserRole] = UserRole.user

    def get_gender_value(self):
        return self.gender.value


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str]
    bio: Optional[str]
    age: Optional[int]
    gender: Optional[Gender]
    hashed_password: Optional[str]


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
