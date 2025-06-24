from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base

class Tag(Base):
    """
    Represents a single tag corresponding to a specific bug record.

    Attributes:
        id (int): Primary key for the tag.
        name (str): Name of the tag.
        bug_id (int): Foreign key to corresponding bug record.
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    bug_id = Column(Integer, ForeignKey("bugs.id"))
    bug = relationship("Bug", back_populates="bugs")