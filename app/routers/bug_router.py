from fastapi import APIRouter
from app.schemas.bug import BugResponse, BugCreate
from app.services.bug import create_bug, get_all_bugs

router = APIRouter()

@router.post("/bugs", response_model=BugResponse)
def create_bug_endpoint(bug: BugCreate):
    new_bug = create_bug(bug)
    return new_bug

@router.get("/bugs")
def get_all_bugs_endpoint():
    bugs = get_all_bugs()
    return [BugResponse.model_validate(bug) for bug in bugs]
