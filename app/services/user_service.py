from sqlalchemy.orm import Session
from schema.user import UserCreate, UserLogin, UserOut, UserUpdate
from repository import user_repo
from fastapi import HTTPException


def create_user_service(db: Session, user_data: UserCreate):
    return user_repo.create_user(db, user_data)


def get_all_user_service(db: Session):
    return user_repo.get_all_users(db)


def get_user_service(db: Session, user_id: id):
    user = user_repo.get_user_by_id(db, user_id)
    print("-------------------------------------------------------------------", user)
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user


def update_user_service(db: Session, user_id: id, user_data: UserUpdate):
    user = user_repo.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user


def delete_user_service(db: Session, user_id: id):
    success = user_repo.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not Found")
    return {"details": "User deleted Successfully"}


# Email : Background Task
from util.email_utils import send_email


def send_welcome_email(email: str):
    subject = "Welcome to our platform!"
    body = f"""
    Hi there!

    🎉 Thank you for registering at our platform.
    We're excited to have you on board!

    Regards,
    Your App Team
    """
    send_email(email, subject, body)
