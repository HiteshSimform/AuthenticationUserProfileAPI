from model.user import User
from schema.user import UserCreate, UserOut, UserUpdate
from sqlalchemy.orm import Session


def create_user(db: Session, user_data: UserCreate) -> UserOut:
    """
    The function creates a new user in the database using the provided user data.

    :param db: The `db` parameter is of type `Session`, which is likely an instance of a database
    session that allows interaction with the database. It is used to perform operations like adding,
    committing, and refreshing data in the database
    :type db: Session
    :param user_data: The `user_data` parameter is of type `UserCreate`, which likely contains data
    needed to create a new user. It seems to have a method `model_dump()` that returns a dictionary or
    model representation of the user data
    :type user_data: UserCreate
    :return: The function `create_user` is returning an instance of `UserOut`.
    """
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# The class `UserRole` defines an enumeration for different user roles such as USER, ADMIN, MODERATOR,
# and MANAGER.


def get_user_by_id(db: Session, user_id: int) -> UserOut:
    """
    This function retrieves a user from the database by their ID while ensuring they are not marked as
    deleted.

    :param db: The `db` parameter is of type `Session`, which is likely an instance of a database
    session that allows you to interact with the database. It is used to query the database to retrieve
    a specific user by their ID
    :type db: Session
    :param user_id: The `user_id` parameter is an integer representing the unique identifier of a user
    in the database
    :type user_id: int
    :return: a user object with the specified user_id from the database, where the user is not marked as
    deleted.
    """
    return db.query(User).filter(User.id == str(user_id), User.is_deleted is False).first()


def get_all_users(db: Session):
    """
    This function retrieves all non-deleted users from a database session.

    :param db: Session
    :type db: Session
    :return: A list of all users from the database where the `is_deleted` attribute is set to `False`.
    """
    return db.query(User).filter(User.is_deleted is False).all()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> UserOut:
    """
    The function `update_user` updates a user's data in the database based on the provided user ID and
    user data.

    :param db: The `db` parameter is of type `Session`, which is likely an instance of a database
    session that allows you to interact with the database. It is used to query and update data in the
    database
    :type db: Session
    :param user_id: The `user_id` parameter is an integer that represents the unique identifier of the
    user whose information needs to be updated in the database
    :type user_id: int
    :param user_data: The `user_data` parameter in the `update_user` function seems to be an instance of
    `UserUpdate` class. This class likely contains data that needs to be updated for a user in the
    database. The `model_dump` method is used to serialize the data from the `UserUpdate`
    :type user_data: UserUpdate
    :return: The function `update_user` is returning the updated user object after making changes to its
    attributes based on the provided `user_data`.
    """
    user = get_user_by_id(db, user_id)
    if user:
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    """
    The function `delete_user` marks a user as deleted in the database by setting the `is_deleted` flag
    to True.

    :param db: The `db` parameter is of type `Session`, which is likely referring to a database session
    object used for database operations. It is being passed to the function `delete_user` to interact
    with the database
    :type db: Session
    :param user_id: The `user_id` parameter in the `delete_user` function is an integer that represents
    the unique identifier of the user that you want to delete from the database
    :type user_id: int
    :return: The function `delete_user` returns a boolean value - `True` if the user with the specified
    `user_id` was found and successfully marked as deleted, and `False` if the user was not found in the
    database.
    """
    user = get_user_by_id(db, user_id)
    if user:
        user.is_deleted = True
        db.commit()
        return True
    return False
