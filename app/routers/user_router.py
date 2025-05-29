from typing import List

from dependencies.auth import get_admin_user, get_current_user
from dependencies.db_dependencies import get_db_session
from fastapi import APIRouter, BackgroundTasks, Depends, status
from model.user import User
from schema.user import UserCreate, UserLogin, UserOut, UserUpdate
from services import user_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


# @router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
# def create_user(user_data: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db_session)):
#     background_tasks.add_task(user_service.send_welcome_email, user_data.email)
#     return user_service.create_user_service(db, user_data)

from fastapi.logger import logger


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db_session),
):
    # breakpoint()
    background_tasks.add_task(user_service.send_welcome_email, user_data.email)
    logger.info(f"Background task scheduled: send_welcome_email to {user_data.email}")
    return user_service.create_user_service(db, user_data)


@router.get("/", response_model=List[UserOut])
def get_users(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return user_service.get_all_user_service(db)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return user_service.get_user_service(db, user_id)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return user_service.update_user_service(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return user_service.delete_user_service(db, user_id)
