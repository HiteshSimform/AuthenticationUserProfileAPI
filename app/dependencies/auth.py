from core.jwt import verify_access_token
from dependencies.db_dependencies import get_db_session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from model.user import User
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    """
    The function `get_current_user` retrieves the current user based on the provided access token and
    database session.

    :param token: The `token` parameter is a string that represents the access token used for
    authentication. It is obtained as a dependency using the `oauth2_scheme` dependency, which likely
    handles the validation and decoding of the access token
    :type token: str
    :param db: The `db` parameter in the `get_current_user` function is used to get a database session
    dependency. It is typically used to interact with the database to query and retrieve data related to
    the current user based on the access token provided. The `get_db_session` function is likely a
    dependency that
    :type db: Session
    :return: The function `get_current_user` is returning the user object fetched from the database
    based on the public_id extracted from the access token payload. If the user is not found or the
    token is invalid/expired, appropriate HTTPExceptions are raised.
    """
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired Token")

    user = db.query(User).filter(User.public_id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_admin_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    """
    The function `get_admin_user` checks if the current user is an admin and returns the current user if
    they have the admin role.

    :param current_user: The `current_user` parameter is of type `User` and is obtained by calling the
    `get_current_user` function using the `Depends` dependency injection. This parameter represents the
    user who is currently authenticated and accessing the endpoint
    :type current_user: User
    :param db: The `db` parameter in the `get_admin_user` function is of type `Session` and is obtained
    by depending on the `get_db_session` function. This parameter is used to interact with the database
    within the function
    :type db: Session
    :return: The `get_admin_user` function is returning the `current_user` if the user's role is
    "admin". If the user's role is not "admin", it will raise an HTTPException with a status code of 403
    and the detail message "Admin Only!".
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only!")
    return current_user
