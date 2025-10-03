from sqlalchemy.orm import Session
from src.app.models.user import User
from src.app.schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        user_name = user.user_name,
        email = user.email,
        hashed_password = user.password,
        date_of_birthday = user.date_of_birthday,
        gender = user.gender
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user