from typing import List, Annotated
from pydantic import BaseModel, AfterValidator, Field, model_validator, ValidationError, ConfigDict
from enum import Enum
from datetime import datetime
from pydantic_core import PydanticUndefined

from app.utils.validators import (
    title_must_not_be_empty,
    description_must_not_be_empty, tag_name_must_not_be_empty
)

class Status(str, Enum):
    OPEN="OPEN"
    CLOSED="CLOSED"
    IN_PROGRESS="IN PROGRESS"

class Priority(str, Enum):
    LOW="LOW"
    MEDIUM="MEDIUM"
    HIGH="HIGH"

class Severity(str, Enum):
    MINOR="MINOR"
    MAJOR="MAJOR"
    CRITICAL="CRITICAL"

class TagCreate(BaseModel):
    name: Annotated[str, AfterValidator(tag_name_must_not_be_empty)]

class TagResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

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

    model_config = ConfigDict(from_attributes=True)


class BugUpdate(BaseModel):
    title: Annotated[str, AfterValidator(title_must_not_be_empty)] = Field(default=PydanticUndefined)
    description: Annotated[str, AfterValidator(description_must_not_be_empty)] = Field(default=PydanticUndefined)
    status: Status | None = None
    priority: Priority | None = None
    severity: Severity | None = None
    submitter: str | None = None
    assigned_to: str | None = None
    tags: List[str] | None = None

    @model_validator(mode="before")
    def at_leats_one_field(cls, values):
        if not values or all(v is None for v in values.values()):
            raise ValidationError("PATCH request requires at least one field to update!")
        return values
