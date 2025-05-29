from typing import List

from dependencies.auth import get_current_user
from dependencies.db_dependencies import get_db_session
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.logger import logger
from model.user import User
from schema.user import UserCreate, UserOut, UserUpdate
from services import user_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db_session),
):
    """
    This Python function creates a new user, schedules a background task to send a welcome email, and
    logs the task information.

    :param user_data: The `user_data` parameter is of type `UserCreate`, which likely contains the data
    needed to create a new user. This data could include information such as the user's name, email,
    password, etc. The `UserCreate` model is likely defined somewhere in your codebase and is used
    :type user_data: UserCreate
    :param background_tasks: The `background_tasks` parameter in the `create_user` function is used to
    schedule background tasks to be executed asynchronously. In this case, a welcome email is being sent
    to the user's email address using the `user_service.send_welcome_email` function. By adding the task
    to the `background
    :type background_tasks: BackgroundTasks
    :param db: The `db` parameter in the `create_user` function is of type `Session` and is used to
    interact with the database. It is obtained using the `get_db_session` dependency, which likely
    provides a database session for the function to use when interacting with the database. This
    parameter is essential
    :type db: Session
    :return: The `create_user` function is returning the result of calling the `create_user_service`
    function from the `user_service` module with the database session (`db`) and the user data
    (`user_data`) as arguments. The return value is of type `UserOut` and the HTTP status code is set to
    201 (Created).
    """
    background_tasks.add_task(user_service.send_welcome_email, user_data.email)
    logger.info(f"Background task scheduled: send_welcome_email to {user_data.email}")
    return user_service.create_user_service(db, user_data)


@router.get("/", response_model=List[UserOut])
def get_users(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    This function retrieves all users from the database and returns them as a list of UserOut objects.

    :param db: The `db` parameter is of type `Session` and is used to interact with the database. It is
    injected into the `get_users` function using the `Depends` function, which retrieves the database
    session for the current request. This allows the function to perform database operations such as
    querying for
    :type db: Session
    :param current_user: The `current_user` parameter in the `get_users` function is a dependency that
    is obtained by calling the `get_current_user` function. This dependency is used to retrieve the
    currently authenticated user before accessing the list of users. It ensures that only authenticated
    users can access the list of users
    :type current_user: User
    :return: A list of user objects with the specified fields defined in the UserOut model is being
    returned.
    """
    return user_service.get_all_user_service(db)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    This function retrieves a user's information by their ID from the database and requires
    authentication of the current user.

    :param user_id: The `user_id` parameter in the `get_user` function represents the unique identifier
    of the user whose information is being requested. This parameter is expected to be an integer value
    :type user_id: int
    :param db: The `db` parameter in the `get_user` function is of type `Session` and is used to
    interact with the database. It is obtained using the `Depends` function with the `get_db_session`
    dependency, which likely provides a database session for the function to use. This session
    :type db: Session
    :param current_user: The `current_user` parameter in the `get_user` function is of type `User`,
    which is obtained by calling the `get_current_user` dependency. This parameter represents the
    currently authenticated user who is making the request to fetch the user information identified by
    the `user_id`. It is used for
    :type current_user: User
    :return: The `get_user` function is returning the user data for the user with the specified
    `user_id`. The data is fetched from the database using the `user_service.get_user_service` function.
    The response is expected to be in the format defined by the `UserOut` model.
    """
    return user_service.get_user_service(db, user_id)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    This Python function updates a user's information in a database and requires authentication of the
    current user.

    :param user_id: The `user_id` parameter in the `update_user` function represents the unique
    identifier of the user that you want to update. This identifier is typically an integer value that
    helps identify the specific user record in the database that needs to be updated
    :type user_id: int
    :param user_data: The `user_data` parameter in the `update_user` function represents the data that
    will be used to update the user information in the database. It is of type `UserUpdate`, which
    likely contains fields that can be updated for a user, such as their name, email, or any other
    relevant
    :type user_data: UserUpdate
    :param db: The `db` parameter in the `update_user` function is of type `Session` and is used to
    interact with the database. It is obtained using the `Depends` function with the `get_db_session`
    function as a dependency. This parameter allows the function to perform database operations such as
    :type db: Session
    :param current_user: The `current_user` parameter in the `update_user` function is a dependency that
    is used to get the current user making the request. It is of type `User` and is obtained by calling
    the `get_current_user` function. This parameter is used to ensure that only authenticated users can
    update
    :type current_user: User
    :return: The `update_user` function is returning the result of calling the `update_user_service`
    function from the `user_service` module with the provided parameters `db`, `user_id`, and
    `user_data`. The return value is likely an updated user object based on the changes specified in the
    `user_data` parameter.
    """
    return user_service.update_user_service(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """
    This function deletes a user with the specified user_id from the database.

    :param user_id: The `user_id` parameter in the `delete_user` function represents the unique
    identifier of the user that you want to delete from the database. This parameter is expected to be
    an integer value
    :type user_id: int
    :param db: The `db` parameter is an instance of a database session that is injected into the
    `delete_user` function using a dependency. It is used to interact with the database to perform
    operations such as deleting a user record based on the `user_id` provided. The `get_db_session`
    function is
    :type db: Session
    :param current_user: The `current_user` parameter in the `delete_user` function is of type `User`
    and is obtained by using the `Depends` function with the `get_current_user` dependency. This
    parameter represents the currently authenticated user who is making the request to delete a user
    with the specified `user
    :type current_user: User
    :return: The `delete_user` function is returning the result of calling the `delete_user_service`
    function from the `user_service` module with the provided `db` session and `user_id` as arguments.
    The return value of this function call will be returned as the response from the `delete_user`
    endpoint.
    """
    return user_service.delete_user_service(db, user_id)
