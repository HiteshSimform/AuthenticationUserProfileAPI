from dependencies.auth import get_admin_user, get_current_user
from dependencies.db_dependencies import get_db_session
from fastapi import APIRouter, Depends
from model.user import User
from schema.user import UserOut, UserUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/", response_model=UserOut)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    The function `update_profile` updates the profile of the current user with the provided user update
    data.

    :param user_update: The `user_update` parameter in the `update_profile` function is of type
    `UserUpdate`, which likely contains the data that the user wants to update in their profile. This
    data is used to update the corresponding fields in the `current_user` object
    :type user_update: UserUpdate
    :param db: The `db` parameter in the `update_profile` function is an instance of a database session.
    It is used to interact with the database to update the user's profile information. The `Session`
    type indicates that it is likely an instance of a database session provided by an ORM (Object-Rel
    :type db: Session
    :param current_user: The `current_user` parameter in the `update_profile` function represents the
    user who is currently authenticated and making the request to update their profile. This parameter
    is of type `User`, which likely contains information about the authenticated user such as their
    username, email, and other profile details
    :type current_user: User
    :return: The `update_profile` function is returning the updated `current_user` object after the
    changes have been applied to its attributes based on the values provided in the `user_update`
    object.
    """
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/admin", response_model=UserOut)
def admin_access(current_user: User = Depends(get_admin_user)):
    """
    The function `admin_access` requires an admin user to access the "/admin" route and returns the
    current admin user.

    :param current_user: The `current_user` parameter in the `admin_access` function is of type `User`
    and is obtained by using the `Depends` function with the `get_admin_user` dependency. This means
    that the function `get_admin_user` is responsible for providing the `current_user` object,
    :type current_user: User
    :return: The function `admin_access` is returning the `current_user` object, which is of type
    `UserOut`.
    """
    return current_user


@router.get("/users")
def get_all_users(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db_session)):
    """
    This function retrieves all non-deleted users from the database with the help of the
    `get_admin_user` and `get_db_session` dependencies.

    :param current_user: The `current_user` parameter is of type `User` and is obtained by calling the
    `get_admin_user` function using the `Depends` dependency injection. This parameter represents the
    currently authenticated user who is accessing the endpoint
    :type current_user: User
    :param db: The `db` parameter in the function `get_all_users` is of type `Session` and is used to
    interact with the database. It is obtained by calling the `get_db_session` dependency function. This
    parameter is responsible for managing the database session within the scope of the function
    :type db: Session
    :return: The function `get_all_users` is returning a list of all users from the database where the
    `is_deleted` attribute is set to `False`.
    """
    users = db.query(User).filter(User.is_deleted is False).all()
    return users
