from datetime import datetime
from sqlalchemy.orm import Session
from src.app.models.user import Perfomer
from src.app.services.user_service import UserService

class PerformerService(UserService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_performer(self, user_create):
        hashed_pwd = self.create_base_user(user_create)
        dob = datetime.strptime(user_create.date_of_birthday, "%Y-%m-%d").date()

        performer = Perfomer(
            user_name = user_create.user_name,
            email = user_create.email,
            hashed_password = hashed_pwd,
            date_of_birthday = dob,
            gender = user_create.gender,
            stage_name = getattr(user_create, 'stage_name', None),
            album_count = getattr(user_create, 'album_count', 0)
        )

        self.db.add(performer)
        self.db.commit()
        self.db.refresh(performer)

        return performer