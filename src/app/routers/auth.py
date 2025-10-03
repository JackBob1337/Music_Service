from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.app.database.session import get_db
from src.app.schemas.user import ListenerCreate, PerformerCreate, UserResponse, ListenerResponse, PerformerResponse
from src.app.services.listener_service import ListenerService
from src.app.services.performer_service import PerformerService

router = APIRouter()

# @router.post("/register", response_model=UserResponse)
# def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     from src.app.models.user import User
#     db_user = db.query(User).filter(User.email == user.email).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     db_user_name = db.query(User).filter(User.user_name == user.user_name).first()
#     if db_user_name:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     return create_user(db=db, user=user)


@router.post("/register/listener", response_model=ListenerResponse)
def register_listener(user: ListenerCreate, db: Session = Depends(get_db)):
    service = ListenerService(db)
    listener = service.create_listener(user)
    return ListenerResponse.from_orm(listener)

@router.post("/register/performer", response_model=PerformerResponse)
def register_performer(user: PerformerCreate, db: Session = Depends(get_db)):
    service = PerformerService(db)
    performer = service.create_performer(user)
    return PerformerResponse.from_orm(performer)
