from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    The function `hash_password` takes a password as input and returns the hashed version of the
    password using a password hashing context.

    :param password: The `hash_password` function takes a password as input and returns the hashed
    version of the password using the `pwd_context` object. The `pwd_context` object is assumed to be a
    password hashing library or module that provides a secure way to hash passwords
    :type password: str
    :return: The `hash_password` function is returning the hashed version of the input `password` string
    using the `pwd_context` hashing function.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    The function `verify_password` compares a plain text password with a hashed password to determine if
    they match.

    :param plain_password: The `plain_password` parameter is the password entered by the user in plain
    text, before it is hashed for security purposes
    :type plain_password: str
    :param hashed_password: The `hashed_password` parameter is a string that represents the hashed
    version of a password. Hashing is a process of converting a plain text password into a unique string
    of characters using a cryptographic hash function. This hashed password is typically stored in a
    database for security reasons, instead of storing the actual plain
    :type hashed_password: str
    :return: a boolean value, indicating whether the plain password matches the hashed password after
    verification.
    """
    return pwd_context.verify(plain_password, hashed_password)
