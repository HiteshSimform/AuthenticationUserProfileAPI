from fastapi import APIRouter, Depends, HTTPException, Form

# from sqlalchemy.orm import Session
# from schema.user import UserCreate, UserLogin
# from core.security import hash_password, verify_password
# from model.user import User
# from db.sessions import PostgresSessionLocal, SQLiteSessionLocal
# from config.config import settings
# from core.jwt import create_access_token
# from dependencies.db_dependencies import get_db_session
# from typing import Annotated
# from fastapi.security import OAuth2PasswordRequestForm
# router = APIRouter(prefix="/auth",tags = ["Authentication"])


# # @router.post("/register")
# # def register(user_data:UserCreate,db: Session = Depends(get_db_session)):
# #     user = db.query(User).filter(User.email == user_data.email).first()
# #     if user:
# #         raise HTTPException(status_code=400, detail="Email already exist")
# #     user_data.hashed_password = hash_password(user_data.hashed_password)
# #     user = User(**user_data.model_dump())
# #     db.add(user)
# #     db.commit()
# #     db.refresh(user)
# #     return {"msg":"User registered successfully"}

# from util.emails import send_registration_email
# @router.post("/register")
# def register(user_data:UserCreate,db: Session = Depends(get_db_session)):
#     user = db.query(User).filter(User.email == user_data.email).first()
#     if user:
#         raise HTTPException(status_code=400, detail="Email already exist")

#     user_data.hashed_password = hash_password(user_data.hashed_password)
#     user = User(**user_data.model_dump())
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     # Trigger async task
#     send_registration_email.delay(user.email, user.username)

#     return {"msg":"User registered successfully"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schema.user import UserCreate, UserLogin
from model.user import User
from core.security import hash_password, verify_password
from dependencies.db_dependencies import get_db_session
from core.jwt import create_access_token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

# from util.emails import send_registration_email
from config.celery_worker import send_registration_email

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_data.hashed_password = hash_password(user_data.hashed_password)
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    # Trigger Celery task
    send_registration_email.delay(user.email, user.username)

    return {"msg": "User registered successfully"}


@router.post("/login")
def login(
    user_credentials: Annotated[UserLogin, Form()],
    db: Session = Depends(get_db_session),
):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token = create_access_token(data={"sub": user.public_id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
