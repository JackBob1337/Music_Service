from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.app.models.user import User
from src.app.core.security import hash_password

class UserService():
    def __init__ (self, db: Session):
        self.db = db

    def create_base_user(self, user_create):
        existing_user = self.db.query(User).filter(
            (User.email == user_create.email) | (User.user_name == user_create.user_name)
        ).first()
        if existing_user:
            if existing_user.email == user_create.email:
                raise HTTPException(status_code=400, detail="Email already registered")
            else:
                raise HTTPException(status_code=400, detail="Username already registered")
            
        hashed_pwd = hash_password(user_create.password)

        return hashed_pwd
            