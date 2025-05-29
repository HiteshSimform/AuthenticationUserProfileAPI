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
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/admin", response_model=UserOut)
def admin_access(current_user: User = Depends(get_admin_user)):
    return current_user


@router.get("/users")
def get_all_users(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db_session)):
    users = db.query(User).filter(User.is_deleted is False).all()
    return users
