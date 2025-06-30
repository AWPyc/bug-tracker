from typing import List, Annotated
from pydantic import BaseModel, AfterValidator
from enum import Enum
from datetime import datetime

from app.utils.validators import (
    title_must_not_be_empty,
    description_must_not_be_empty, tag_name_must_not_be_empty
)

class Status(str, Enum):
    OPEN=1
    CLOSED=2
    IN_PROGRESS=3

class Priority(str, Enum):
    LOW=1
    MEDIUM=2
    HIGH=3

class Severity(str, Enum):
    MINOR=1
    MAJOR=2
    CRITICAL=3

class TagCreate(BaseModel):
    id: int
    name: Annotated[str, AfterValidator(tag_name_must_not_be_empty)]

class TagResponse(BaseModel):
    id: int
    name: str

class BugCreate(BaseModel):
    title: Annotated[str, AfterValidator(title_must_not_be_empty)]
    description: Annotated[str, AfterValidator(description_must_not_be_empty)]
    status: Status
    priority: Priority
    severity: Severity
    submitter: str | None
    assigned_to: str | None
    tags: List[str] | None

class BugResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    submitter: str
    title: str
    description: str
    status: Status
    priority: Priority
    severity: Severity
    assigned_to: str | None
    tags: List[TagResponse] | None

    class Config:
        from_attributes = True
