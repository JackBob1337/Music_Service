from datetime import datetime
from sqlalchemy.orm import Session
from src.app.models.user import Listener
from src.app.services.user_service import UserService

class ListenerService(UserService):
    def __init__ (self, db: Session):
        super().__init__(db)

    def create_listener(self, user_create):
        hashed_pwd = self.create_base_user(user_create)

        dob = datetime.strptime(user_create.date_of_birthday, "%Y-%m-%d").date()

        listener = Listener(
            user_name = user_create.user_name,
            email = user_create.email,
            hashed_password = hashed_pwd,
            date_of_birthday = dob,
            gender = user_create.gender,
            favorite_genre = getattr(user_create, 'favorite_genre', None)            
        )

        self.db.add(listener)
        self.db.commit()
        self.db.refresh(listener)

        return listener

