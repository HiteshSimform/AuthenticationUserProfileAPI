from fastapi import HTTPException
from repository import user_repo
from schema.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session
from util.email_utils import send_email


def create_user_service(db: Session, user_data: UserCreate):
    """
    The function `create_user_service` creates a new user in the database using the provided user data.

    :param db: The `db` parameter is of type `Session`, which likely refers to a database session object
    used for database operations. It is typically used to interact with the database to perform
    operations like creating, updating, or querying data
    :type db: Session
    :param user_data: The `user_data` parameter in the `create_user_service` function likely contains
    the data needed to create a new user. This data could include information such as the user's
    username, email, password, and any other relevant details required to create a user account
    :type user_data: UserCreate
    :return: The `create_user_service` function is returning the result of calling the `create_user`
    function from the `user_repo` module with the provided database session (`db`) and user data
    (`user_data`).
    """
    return user_repo.create_user(db, user_data)


def get_all_user_service(db: Session):
    """
    The function `get_all_user_service` retrieves all users from the database.

    :param db: The `db` parameter is of type `Session`, which is likely referring to a database session
    object. This parameter is used to interact with the database within the `get_all_user_service`
    function
    :type db: Session
    :return: The function `get_all_user_service` is returning all users from the database by calling the
    `get_all_users` function from the `user_repo` module.
    """
    return user_repo.get_all_users(db)


def get_user_service(db: Session, user_id: int):
    """
    The function `get_user_service` retrieves a user from the database based on the provided user ID.

    :param db: The `db` parameter is of type `Session`, which is likely a database session object used
    for interacting with the database. It is typically used to perform database operations like
    querying, updating, or deleting data
    :type db: Session
    :param user_id: The `user_id` parameter is an integer value that represents the unique identifier of
    a user in the database. It is used to retrieve a specific user's information from the database
    :type user_id: int
    :return: The function `get_user_service` is returning the user object fetched from the database
    based on the provided `user_id`. If the user is not found in the database, it will raise an
    HTTPException with a status code of 404 and a detail message of "User not Found".
    """
    user = user_repo.get_user_by_id(db, user_id)
    print("-------------------------------------------------------------------", user)
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user


def update_user_service(db: Session, user_id: int, user_data: UserUpdate):
    """
    This function updates user data in a database and returns the updated user information, raising a
    404 error if the user is not found.

    :param db: The `db` parameter is of type `Session`, which is likely referring to a database session
    object used for interacting with the database. It is commonly used in SQLAlchemy to perform database
    operations within a session context
    :type db: Session
    :param user_id: The `user_id` parameter is an integer that represents the unique identifier of the
    user whose information is being updated in the database
    :type user_id: int
    :param user_data: The `user_data` parameter in the `update_user_service` function likely represents
    the data that is being used to update a user's information. This data could include fields such as
    the user's name, email, password, or any other information that can be updated for a user in the
    system
    :type user_data: UserUpdate
    :return: The function `update_user_service` is returning the updated user data after updating it in
    the database. If the user is not found in the database, it raises an HTTPException with a status
    code of 404 and the detail message "User not Found".
    """
    user = user_repo.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user


def delete_user_service(db: Session, user_id: int):
    """
    This function deletes a user from the database and returns a success message or raises a 404 error
    if the user is not found.

    :param db: The `db` parameter is of type `Session`, which is likely referring to a database session
    object. This object is used to interact with the database and perform operations such as querying,
    updating, and deleting data. In this context, it is being passed to the `delete_user_service`
    function to
    :type db: Session
    :param user_id: The `user_id` parameter is an integer that represents the unique identifier of the
    user that you want to delete from the database
    :type user_id: int
    :return: {"details": "User deleted Successfully"}
    """
    success = user_repo.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not Found")
    return {"details": "User deleted Successfully"}


# Email : Background Task


def send_welcome_email(email: str):
    """
    The function `send_welcome_email` sends a welcome email to a user who has registered on a platform.

    :param email: The `send_welcome_email` function is designed to send a welcome email to a user who
    has registered on your platform. The function takes the user's email address as a parameter
    :type email: str
    """
    subject = "Welcome to our platform!"
    body = """
    Hi there!

    Thank you for registering at our platform.
    We're excited to have you on board!

    Regards,
    Your App Team
    """
    send_email(email, subject, body)
