import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.testclient import TestClient
from app.main import app
from app.db.session import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)

def override_get_db():
    with SessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session_client(): # to moj hanlder który dodałem
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        yield session
    Base.metadata.drop_all(bind=engine)

