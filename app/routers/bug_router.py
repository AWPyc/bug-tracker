from fastapi import HTTPException
from fastapi import APIRouter
from app.schemas.bug import BugResponse, BugCreate
from app.services.bug import create_bug, get_all_bugs, get_bug_by_id

router = APIRouter()

@router.post("/bugs", response_model=BugResponse, status_code=201)
def create_bug_endpoint(bug: BugCreate):
    """
    Create bug record.
    """
    new_bug = create_bug(bug)
    return new_bug

@router.get("/bugs")
def get_all_bugs_endpoint():
    """
    Get a list of all bug records.
    Returns 404 if bugs do not exist.
    """
    bugs = get_all_bugs()
    if not bugs:
        return []
    return [BugResponse.model_validate(bug) for bug in bugs]

@router.get("/bug/{bug_id}", response_model=BugResponse)
def get_bug_endpoint(bug_id: int):
    """
    Get a single bug record by its ID.
    Returns 404 if the bug does not exist.
    """
    bug = get_bug_by_id(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail=f"Bug with specified id:{bug_id} does not exist!")
    return BugResponse.model_validate(bug)
