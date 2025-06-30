from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.session import Base

bug_tags = Table(
    "bug_tags",
    Base.metadata,
    Column("bug_id", Integer, ForeignKey("bugs.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)