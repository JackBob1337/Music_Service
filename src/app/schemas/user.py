from pydantic import BaseModel, EmailStr, field_validator
from pydantic import ConfigDict
from typing import Optional
from uuid import UUID

from src.app.core.security import password_validation, user_name_validator

class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    date_of_birthday: str
    gender: str

    @field_validator('password')
    def validate_password(cls, pwd):
        password_validation(pwd)
        return pwd
    
    @field_validator('user_name')
    def validate_user_name(cls, v: str):
        user_name_validator(v)
        return v.strip()

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
