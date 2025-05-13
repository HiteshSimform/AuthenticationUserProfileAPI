from fastapi import APIRouter, Depends, status
from typing import List
from schema.user import UserCreate, UserLogin, UserOut, UserUpdate
from sqlalchemy.orm import Session
from services import user_service
from dependencies.db_dependencies import get_db_session

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db:Session = Depends(get_db_session)):
    return user_service.create_user_service(db,user_data)

@router.get("/",response_model=List[UserOut])
def get_users(db: Session=Depends(get_db_session)):
    return user_service.get_all_user_service(db)