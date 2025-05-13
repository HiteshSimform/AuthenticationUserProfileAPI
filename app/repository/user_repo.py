from sqlalchemy.orm import Session
from model.user import User
from schema.user import UserCreate, UserLogin, UserOut, UserUpdate


def create_user(db: Session, user_data: UserCreate) -> UserOut:
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> UserOut:
    return db.query(User).filter(User.id == str(user_id), User.is_deleted == False).first() 


def get_all_users(db: Session):
    return db.query(User).filter(User.is_deleted == False).all()

def update_user(db: Session, user_id: id, user_data: UserUpdate) -> UserOut:
    user=  get_user_by_id(db,str(user_id))
    if user:
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user,key,value)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if user:
        user.is_deleted = True
        db.commit()
        return True
    return False