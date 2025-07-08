import os
from contextlib import contextmanager
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from app.main import app
from app.db.session import get_db, Base
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    with SessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@contextmanager
def restart_db():
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    with restart_db():
        yield TestClient(app)

@pytest.fixture(scope="function")
def session_client():
    with restart_db():
        with SessionLocal() as session:
            yield session

