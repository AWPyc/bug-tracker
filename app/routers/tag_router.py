from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.bug import TagResponse
from app.services.tag import get_all_tags

router = APIRouter()

@router.get("/tags", response_model=List[TagResponse], status_code=200)
def get_all_tags_endpoint(session: Session = Depends(get_db)) -> List[TagResponse]:
    """
    Retrieve all tag records.

    Args:
        session (Session, optional): DB session.

    Returns:
        List[TagResponse]: List of all tags or empty list if none exist.
    """
    tags = get_all_tags(session)
    if not tags:
        return []
    return [TagResponse.model_validate(tag) for tag in tags]