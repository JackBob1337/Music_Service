from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    sub: str
    exp: int

class TrackCreate(BaseModel):
    title: str
    file_path: str


