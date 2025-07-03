from datetime import datetime, timezone
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.models.association import bug_tags
from app.db.session import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from app.schemas.bug import Status, Priority, Severity


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
        submitter (str): User reporting the bug.
        created_at (datetime): The time bug record was created.
        updated_at (datetime): The time bug record was modified.
        tags (list[str]): Corresponding tags to the bug record.
    """
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(Status), nullable=False)
    priority = Column(SQLAlchemyEnum(Priority), nullable=False)
    severity = Column(SQLAlchemyEnum(Severity), nullable=False)
    assigned_to = Column(String, nullable=True)
    submitter = Column(String, nullable=False, default="system")
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    tags = relationship("Tag", secondary=bug_tags, back_populates="bugs")

