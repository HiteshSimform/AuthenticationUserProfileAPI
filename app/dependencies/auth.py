from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.jwt import verify_access_token
from sqlalchemy.orm import Session
from db.sessions import PostgresSessionLocal, SQLiteSessionLocal
from config.config import settings
from model.user import User
from dependencies.db_dependencies import get_db_session
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)
):
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
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only!")
    return current_user


# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from core.jwt import verify_access_token
# from sqlalchemy.orm import Session
# from db.sessions import PostgresSessionLocal, SQLiteSessionLocal
# from config.config import settings
# from model.user import User
# from dependencies.db_dependencies import get_db_session
# import jwt

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
#     try:
#         payload = verify_access_token(token)
#         if not payload:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token payload",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token has expired",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     except jwt.PyJWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     user = db.query(User).filter(User.public_id == payload.get("sub")).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     return user, token

# def get_admin_user(current_user: User = Depends(get_current_user)):
#     if current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Admins only!"
#         )
#     return current_user
