import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    The function `create_access_token` generates a JWT access token with optional expiration time.

    :param data: The `data` parameter is a dictionary containing the information that you want to encode
    into the access token. This information could include user details, permissions, or any other data
    you want to associate with the token
    :type data: dict
    :param expires_delta: The `expires_delta` parameter is used to specify the duration for which the
    access token will remain valid. If a value is provided for `expires_delta`, the access token will
    expire after the specified duration. If no value is provided, the access token will expire after 15
    minutes by default
    :type expires_delta: timedelta | None
    :return: The function `create_access_token` returns an encoded JSON Web Token (JWT) containing the
    data provided in the `data` dictionary along with an expiration time.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def verify_access_token(token: str):
    """
    The function `verify_access_token` decodes a JWT token using a secret key and algorithm, returning
    the payload if successful or None if an error occurs.

    :param token: The `token` parameter is a string that represents an access token that needs to be
    verified for authentication purposes
    :type token: str
    :return: The `verify_access_token` function is returning the decoded payload if the access token is
    successfully decoded using the `jwt.decode` method with the provided `SECRET_KEY` and `ALGORITHM`.
    If there is a `JWTError` exception raised during the decoding process, the function will return
    `None`.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
