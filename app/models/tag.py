from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.association import bug_tags
from app.db.session import Base

class Tag(Base):
    """
    Represents a single tag corresponding to a specific bug record.

    Attributes:
        id (int): Primary key for the tag.
        name (str): Name of the tag.
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    bugs = relationship("Bug", secondary=bug_tags, back_populates="tags")