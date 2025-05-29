from core.jwt import verify_access_token
from dependencies.db_dependencies import get_db_session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from model.user import User
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
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
