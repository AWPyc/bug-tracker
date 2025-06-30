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
            if bug.tags:
                for tag in bug.tags:
                    tag_record = Tag(name=tag)
                    bug_record.tags.append(tag_record)
            session.add(bug_record)
            session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Unable to create Bug record: {e}. Rolling back.")
            session.rollback()
            raise e
    return bug_record

def get_all_bugs() -> List[Bug]:
    with SessionLocal() as session:
        try:
            bugs_list = session.query(Bug).options(joinedload(Bug.tags)).all()
            return bugs_list
        except SQLAlchemyError as e:
            logging.error(f"Unable to fetch Bug records {e}.")
            raise e

def get_bug_by_id(bug_id: int) -> Bug:
    with SessionLocal() as session:
        try:
            bug = session.query(Bug).options(joinedload(Bug.tags)).filter(Bug.id == bug_id).first()
            return bug
        except SQLAlchemyError as e:
            logging.error(f"Unable to fetch Bug record with ID:{bug_id}")
            raise e

