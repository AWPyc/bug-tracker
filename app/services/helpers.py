from enum import Enum
from datetime import datetime, timezone
from typing import Optional, List
from app.models.bug import Bug
from app.models.tag import Tag
from app.schemas.bug import BugCreate, BugUpdate


class Operation(Enum):
    CREATE = "CREATE"
    PATCH = "PATCH"
    PUT = "PUT"

def apply_bug_data_to_model(bug_obj: Bug, data: Optional[BugCreate | BugUpdate], operation: Operation = Operation.CREATE) -> None:
    """
    Applies BugCreate data to a Bug model instance.
    Tags are handled separately.
    Args:
        bug_obj (Bug): Bug ORM object to update.
        data (BugCreate | BugUpdate): Incoming data from the request.
        operation (Operation): Determines how to apply data (CREATE, PATCH, PUT).

    Returns:
        None
    """
    if operation == Operation.PATCH:
        data_dict = data.model_dump(exclude_unset=True)
        bug_obj.updated_at = datetime.now(timezone.utc)
    else:
        data_dict = data.model_dump()

    for field, value in data_dict.items():
        if field == "tags":
            continue
        setattr(bug_obj, field, value)

def assign_tags_to_bug(bug: Bug, tags: List[Tag], operation: Operation = Operation.CREATE) -> None:
    """
    Assigns Tag objects to a Bug model instance.

    Args:
        bug (Bug): Bug ORM object to update.
        tags (List[Tag]): Tag ORM objects list to assign to the bug.
        operation (Operation): Determines how to apply data (CREATE, PATCH, PUT).

    Returns:
        None
    """
    if operation == Operation.PATCH:
        existing_tags = {tag.id for tag in bug.tags}
        new_tags = [tag for tag in tags if tag.id not in existing_tags]
        bug.tags.extend(new_tags)
    else:
        bug.tags = tags
