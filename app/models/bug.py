from datetime import datetime

from sqlalchemy.orm import relationship

from app.db.session import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

class Bug(Base):
    """
    Represents a bug record in the system.

    Attributes:
        id (int): Primary key for the bug record.
        title (str): Title for the bug record.
        description (str): Description of the bug record.
        status (str): Current bug status.
        priority (str): Priority level of the bug.
        severity (str): Severity level of the bug.
        created_at (datetime): The time bug record was created.
        updated_at (datetime): The time bug record was modified.
        tags (list[str]): Corresponding tags to the bug record.
    """
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    assigned_to = Column(String, nullable=True)
    submitter = Column(String, nullable=False, default="???")
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    tags = relationship("Tag", back_populates="bug", cascade="all, delete-orphan")

