from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from src.app.core.security import create_access_token, create_refresh_token
from src.app.database.session import get_db
from src.app.models.user import Listener, Perfomer
from src.app.schemas.user import ListenerCreate, PerformerCreate, UserResponse, ListenerResponse, PerformerResponse
from src.app.schemas.auth import LoginRequest
from src.app.services.user_service import UserService
from src.app.services.listener_service import ListenerService
from src.app.services.performer_service import PerformerService

router = APIRouter()

@router.post("/register/listener", summary="Create a listener", response_model=ListenerResponse)
def register_listener(user: ListenerCreate, db: Session = Depends(get_db)):
    service = ListenerService(db)
    listener = service.create_listener(user)
    return ListenerResponse.from_orm(listener)

@router.post("/register/performer", response_model=PerformerResponse)
def register_performer(user: PerformerCreate, db: Session = Depends(get_db)):
    service = PerformerService(db)
    performer = service.create_performer(user)
    return PerformerResponse.from_orm(performer)

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.login_user(email, password)
    
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }

        
@router.get("/listeners")
def get_listeners(db: Session = Depends(get_db)):
    return db.query(Listener).all()

@router.get("/performers")
def get_performers(db: Session = Depends(get_db)):
    return db.query(Perfomer).all()
