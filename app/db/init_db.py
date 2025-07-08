from app.db.session import Base, engine
from app.models.bug import Bug # noqa
from app.models.tag import Tag # noqa

def init_db():
        Base.metadata.create_all(engine)