from datetime import datetime
from sqlalchemy.orm import Session
from src.app.models.user import Performer, Tracks
from src.app.services.user_service import UserService

class PerformerService(UserService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_performer(self, user_create):
        hashed_pwd = self.create_base_user(user_create)
        dob = datetime.strptime(user_create.date_of_birthday, "%Y-%m-%d").date()

        performer = Performer(
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
    
    def upload_track(self, performer_id: str, track_data):
        performer = self.db.query(Performer).filter(Performer.id == performer_id).first()
        if not performer:
            raise ValueError("Performer not found")

        track = Tracks(
            title = track_data.title,
            genre = getattr(track_data, "genre", None),
            file_path = track_data.file_path,
            performer_id = performer.id
        )

        self.db.add(track)
        self.db.commit()
        self.db.refresh(track)

        return track