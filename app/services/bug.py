from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.db.session import SessionLocal
from app.models.bug import Bug
from app.models.tag import Tag
from app.schemas.bug import BugCreate, BugResponse
from datetime import datetime
import logging

def create_bug(bug: BugCreate) -> Bug:

    with SessionLocal() as session:
        try:
            bug_record = Bug(
                title=bug.title,
                description=bug.description,
                status=bug.status,
                priority=bug.priority,
                severity=bug.severity,
                submitter="system",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(bug_record)
            if bug.tags:
                for tag in bug.tags:
                    tag_record = Tag(name=tag, bug_id=bug_record.id)
                    session.add(tag_record)
            session.commit()
            session.refresh(bug_record)
        except SQLAlchemyError as e:
            logging.error(f"Unable to create Bug record: {e}. Rolling back.")
            session.rollback()
            raise e
    return bug_record

def get_all_bugs() -> List[BugResponse]:
    with SessionLocal() as session:
        try:
            bugs_list = session.query(Bug).options(joinedload(Bug.tags)).all()
            return bugs_list
        except SQLAlchemyError as e:
            logging.error(f"Unable to fetch Bug records {e}.")
            raise e
