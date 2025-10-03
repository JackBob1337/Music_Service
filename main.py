import sys
import os 

from fastapi import FastAPI
from src.app.routers import auth
from src.app.database.session import Base, engine


sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Music Service API")

app.include_router(auth.router)
