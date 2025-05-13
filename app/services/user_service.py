from sqlalchemy.orm import Session
from schema.user import UserCreate, UserLogin, UserOut, UserUpdate
from repository import user_repo
from fastapi import HTTPException


def create_user_service(db: Session, user_data: UserCreate):
    return user_repo.create_user(db, user_data)


def get_all_user_service(db: Session):
    return user_repo.get_all_users(db)

