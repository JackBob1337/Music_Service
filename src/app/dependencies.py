from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.app.core.security import ALGORITHM, JWT_SECRET_KEY
from src.app.schemas.auth import TokenPayload
from src.app.schemas.user import UserResponse
from src.app.models.user import User
from src.app.database.session import get_db

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

async def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user: Union[User, None] = db.query(User).filter(User.id == token_data.sub).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse.from_orm(user)