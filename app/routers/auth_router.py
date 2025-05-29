from typing import Annotated

# from util.emails import send_registration_email
from config.celery_worker import send_registration_email
from core.jwt import create_access_token
from core.security import hash_password, verify_password
from dependencies.db_dependencies import get_db_session
from fastapi import APIRouter, Depends, Form, HTTPException
from model.user import User
from schema.user import UserCreate, UserLogin
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db_session)):
    """
    The function registers a new user in a database, checks if the email already exists, triggers a
    Celery task to send a registration email, and returns a success message.

    :param user_data: The `user_data` parameter in the `register` function is of type `UserCreate`,
    which likely contains data for creating a new user. It may include fields such as `email`,
    `username`, and `hashed_password`. This data is used to check if a user with the same email already
    :type user_data: UserCreate
    :param db: The `db` parameter in the `register` function is a database session object. It is used to
    interact with the database to perform operations like querying, adding, committing, and refreshing
    data. In this case, it is being used to check if a user with the provided email already exists in
    the
    :type db: Session
    :return: a dictionary with a key "msg" and a value "User registered successfully".
    """
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
    """
    The function handles user login by verifying credentials and generating an access token for
    authentication.

    :param user_credentials: The `user_credentials` parameter in the `login` function is of type
    `UserLogin` and is expected to be provided as form data. It likely contains the username and
    password entered by the user when attempting to log in
    :type user_credentials: Annotated[UserLogin, Form()]
    :param db: The `db` parameter in the `login` function is of type `Session` and is obtained by
    calling the `get_db_session` dependency. This parameter is used to interact with the database
    session to query the `User` table and verify the user's credentials during the login process
    :type db: Session
    :return: The login route is returning a dictionary containing an access token and token type. The
    access token is generated using the user's public ID and role, and the token type is set to
    "bearer".
    """
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token = create_access_token(data={"sub": user.public_id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
