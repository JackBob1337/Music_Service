import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from src.app.database.session import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_name = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(128), nullable=False)
    date_of_birthday = Column(Date, nullable=False)
    gender = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }

class Listener(User):
    __tablename__ = 'listeners'

    id = Column(String, ForeignKey('users.id'), primary_key=True)
    favorite_genre = Column(String(50), nullable=True)

    __mapper_args__= {
        'polymorphic_identity': 'listener'
    }

class Performer(User):
    __tablename__ = 'performers'

    id = Column(String, ForeignKey('users.id'), primary_key=True)
    stage_name = Column(String(50), unique=True, nullable=False, index=True)
    album_count = Column(Integer,  default=0)

    tracks = relationship("Tracks", back_populates="performer", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'performer'
    }

class Tracks(Base):
    __tablename__ = 'tracks'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    performer_id = Column(String, ForeignKey('performers.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    performer = relationship("Performer", back_populates="tracks")

    