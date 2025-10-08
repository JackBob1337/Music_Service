import pytest
import os, sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app
from src.app.database.session import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
testing_session_local = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db():
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

