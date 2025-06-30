from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Local base SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./bugtracker.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    with SessionLocal() as session:
        yield session
