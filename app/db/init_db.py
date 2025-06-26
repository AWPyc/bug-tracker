from app.db.session import Base, engine
from app.models.bug import Bug
from app.models.tag import Tag

def init_db():
        Base.metadata.create_all(engine)