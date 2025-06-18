from typing import List, Annotated
from pydantic import BaseModel, AfterValidator
from enum import Enum
from datetime import datetime

from app.utils.validators import (
    title_must_not_be_empty,
    description_must_not_be_empty
)

class Status(Enum):
    OPEN=1
    CLOSED=2
    IN_PROGRESS=3

class Priority(Enum):
    LOW=1
    MEDIUM=2
    HIGH=3

class Severity(Enum):
    MINOR=1
    MAJOR=2
    CRITICAL=3

class BugCreate(BaseModel):
    title: Annotated[str, AfterValidator(title_must_not_be_empty)]
    description: Annotated[str, AfterValidator(description_must_not_be_empty)]
    status: Status
    priority: Priority
    severity: Severity
    assigned_to: str | None
    tags: List[str] | None
    submitter: str | None

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
    tags: List[str] | None
