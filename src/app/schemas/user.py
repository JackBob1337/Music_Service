from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    date_of_birthday: str
    gender: str

class ListenerCreate(UserCreate):
    favorite_genre: Optional[str] = None

class PerformerCreate(UserCreate):
    stage_name: Optional[str] = None
    album_count: Optional[int] = 0

class UserResponse(BaseModel):
    id: UUID
    user_name: str
    email: EmailStr
    type: str

    model_config = ConfigDict(from_attributes=True)  # вместо устаревшего Config

class ListenerResponse(UserResponse):
    favorite_genre: Optional[str] = None

class PerformerResponse(UserResponse):
    stage_name: str
    album_count: Optional[int] = 0
