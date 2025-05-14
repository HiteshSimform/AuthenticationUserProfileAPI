from fastapi import APIRouter, Depends, status
from typing import List
from schema.user import UserCreate, UserLogin, UserOut, UserUpdate
from sqlalchemy.orm import Session
from services import user_service
from dependencies.db_dependencies import get_db_session
from dependencies.auth import get_current_user, get_admin_user
from model.user import User

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db:Session = Depends(get_db_session)):
    return user_service.create_user_service(db,user_data)

@router.get("/",response_model=List[UserOut])
def get_users(db: Session=Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return user_service.get_all_user_service(db)

@router.get("/{user_id}",response_model=UserOut)
def get_user(user_id:int, db:Session=Depends(get_db_session),current_user: User = Depends(get_current_user)):
    return user_service.get_user_service(db,user_id)

@router.put("/{user_id}",response_model=UserOut)
def update_user(user_id:int, user_data: UserUpdate, db: Session=Depends(get_db_session),current_user: User = Depends(get_current_user)):
    return user_service.update_user_service(db,user_id, user_data)

@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int, db:Session=Depends(get_db_session),current_user: User = Depends(get_current_user)):
    return user_service.delete_user_service(db,user_id)