import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, TEXT, Date
from src.app.database.session import Base


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

class Perfomer(User):
    __tablename__ = 'performes'

    id = Column(String, ForeignKey('users.id'), primary_key=True)
    stage_name = Column(String(50), unique=True, nullable=False, index=True)
    album_count = Column(Integer,  default=0)

    __mapper_args__ = {
        'polymorphic_identity': 'perfomer'
    }