from typing import List

from fastapi import HTTPException, Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.bug import BugResponse, BugCreate, BugUpdate
from app.services.bug import create_bug, get_all_bugs, get_bug_by_id, update_bug_partial, update_bug_full

router = APIRouter()

@router.post("/bugs", response_model=BugResponse, status_code=201)
def create_bug_endpoint(bug: BugCreate, session: Session = Depends(get_db)) -> BugResponse:
    """
    Create a new bug record.

    Args:
        bug (BugCreate): Data for the new bug.
        session (Session, optional): DB session.

    Returns:
        BugResponse: Created bug.
    """
    new_bug = create_bug(session, bug)
    return new_bug

@router.get("/bugs", response_model=List[BugResponse])
def get_all_bugs_endpoint(session: Session = Depends(get_db)) -> List[BugResponse]:
    """
    Retrieve all bug records.

    Args:
        session (Session, optional): DB session.

    Returns:
        List[BugResponse]: List of all bugs or empty list if none exist.
    """
    bugs = get_all_bugs(session)
    if not bugs:
        return []
    return [BugResponse.model_validate(bug) for bug in bugs]

@router.get("/bug/{bug_id}", response_model=BugResponse)
def get_bug_endpoint(bug_id: int, session: Session = Depends(get_db)) -> BugResponse:
    """
    Get a bug by its ID.

    Args:
        bug_id (int): ID of the bug.
        session (Session, optional): DB session.

    Raises:
        HTTPException: If bug not found (404).

    Returns:
        BugResponse: Bug data.
    """
    bug = get_bug_by_id(session, bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail=f"Bug with specified id:{bug_id} does not exist!")
    return BugResponse.model_validate(bug)

@router.patch("/bug/{bug_id}", status_code=204)
def update_bug_partial_endpoint(bug_id: int, bug_data: BugUpdate, session: Session = Depends(get_db)) -> None:
    """
    Partially update a bug record. Returns blank response (204) No Content.

    Args:
        bug_id (int): ID of the bug.
        bug_data (BugUpdate): Fields to update.
        session (Session, optional): DB session.

    Raises:
        HTTPException: If bug not found or validation error.
    """
    update_bug_partial(session, bug_id, bug_data)

@router.put("/bug/{bug_id}", status_code=200)
def update_bug_full_endpoint(bug_id: int, bug_data: BugCreate, session: Session = Depends(get_db)) -> BugResponse:
    """
    Fully update a bug record (replace all fields).

    Args:
        bug_id (int): ID of the bug.
        bug_data (BugCreate): New data for the bug.
        session (Session, optional): DB session.

    Raises:
        HTTPException: If bug not found.

    Returns:
        BugResponse: Bug data.
    """
    return update_bug_full(session, bug_id, bug_data)
