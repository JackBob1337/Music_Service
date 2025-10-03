from fastapi import FastAPI
from src.app.routers import auth
from src.app.database.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Music Service API")

app.include_router(auth.router)
