from fastapi import HTTPException
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, Session
from app.models.bug import Bug
from app.models.tag import Tag
from app.schemas.bug import BugCreate, BugUpdate, BugResponse
import logging

from app.services.helpers import apply_bug_data_to_model, Operation, assign_tags_to_bug


def sync_tags(session: Session, bug: Bug, tag_names: list[str], operation: Operation = Operation.CREATE) -> None:
    """
    Synchronize bug.tags with tag objects for given tag_names.
    Creates new Tag objects if they don't exist.

    Args:
        session (Session): DB session
        bug (Bug): Bug ORM object
        tag_names (list[str]): list of tag names
        operation (Operation): Determines how to apply data (CREATE, PATCH, PUT).
    """
    try:
        existing_tags = session.query(Tag).filter(Tag.name.in_(tag_names)).all()
        existing_tag_names = {tag.name for tag in existing_tags}

        new_tag_names = set(tag_names) - existing_tag_names
        new_tags = [Tag(name=name) for name in new_tag_names]

        session.add_all(new_tags)
        session.flush()

        all_new_tags = existing_tags + new_tags

        assign_tags_to_bug(bug, all_new_tags, operation)
    except SQLAlchemyError as e:
        logging.error(f"Unable to assign tags to bug record: {e}. Rolling back.")
        session.rollback()
        raise e

def create_bug(session: Session, bug: BugCreate) -> Bug:
    """
    Create a new Bug record in the database.

    Args:
        session (Session): SQLAlchemy database session.
        bug (BugCreate): Data for creating a bug.

    Returns:
        Bug: The created Bug ORM object.
    """
    try:
        bug_record = Bug()
        apply_bug_data_to_model(bug_record, bug, Operation.CREATE)

        session.add(bug_record)

        if bug.tags:
            sync_tags(session, bug_record, bug.tags, Operation.CREATE)

        session.commit()
        session.refresh(bug_record)

    except SQLAlchemyError as e:
        logging.error(f"Unable to create Bug record: {e}. Rolling back.")
        session.rollback()
        raise e

    return bug_record

def get_all_bugs(session: Session) -> List[Bug]:
    """
    Get list of all Bug records from the database.

    Args:
        session (Session): SQLAlchemy database session.

    Returns:
        List[Bug]: The list of all Bug ORM object.
    """
    try:
        bugs_list = session.query(Bug).options(joinedload(Bug.tags)).all()
        return bugs_list

    except SQLAlchemyError as e:
        logging.error(f"Unable to fetch Bug records {e}.")
        raise e

def get_bug_by_id(session: Session, bug_id: int) -> Bug:
    """
    Get a Bug record from the database by ID.

    Args:
        session (Session): SQLAlchemy database session.
        bug_id (int): ID of the Bug object.

    Returns:
        Bug: The created Bug ORM object.
    """
    try:
        bug = session.query(Bug).options(joinedload(Bug.tags)).filter(Bug.id == bug_id).first()
        return bug
    except SQLAlchemyError as e:
        logging.error(f"Unable to fetch Bug record with ID:{bug_id}")
        raise e

def update_bug_partial(session: Session, bug_id: int, bug_data: BugUpdate) -> None:
    """
    Partially update a bug record with given fields.

    Args:
        session (Session): SQLAlchemy database session.
        bug_id (int): ID of the bug to update.
        bug_data (BugUpdate): Data with fields to update.

    Raises:
        HTTPException: If bug not found or DB error occurs.
    """

    try:
        bug_from_db = get_bug_by_id(session, bug_id)
        if not bug_from_db:
            raise HTTPException(status_code=404, detail="Bug not found")

        apply_bug_data_to_model(bug_from_db, bug_data, Operation.PATCH)
        if bug_data.tags is not None:
            sync_tags(session, bug_from_db, bug_data.tags, Operation.PATCH)

        session.commit()
        session.refresh(bug_from_db)

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Unable to PATCH Bug record with ID:{bug_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

def update_bug_full(session: Session, bug_id: int, bug_data: BugCreate) -> Bug:
    """
    Fully update a bug record with new data.

    Args:
        session (Session): SQLAlchemy database session.
        bug_id (int): ID of the bug to update.
        bug_data (BugCreate): Full data to replace the bug with.

    Raises:
        HTTPException: If bug not found or DB error occurs.

    Returns:
        BugResponse: BugResponse schema with updated data.
    """
    try:
        bug_from_db = get_bug_by_id(session, bug_id)
        if not bug_from_db:
            raise HTTPException(status_code=404, detail="Bug not found")

        apply_bug_data_to_model(bug_from_db, bug_data, Operation.PUT)

        if bug_data.tags is not None:
            sync_tags(session, bug_from_db, bug_data.tags)

        session.commit()
        session.refresh(bug_from_db)

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Unable to PUT Bug record with ID:{bug_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return bug_from_db

def delete_bug(session: Session, bug_id: int) -> None:
    """
    Delete Bug record from the database. (Does not delete related Tag objects - only references).

    Args:
        bug_id (int): ID of the bug.
        session (Session, optional): DB session.

    Raises:
        HTTPException: If bug not found.

    Returns:
        None.
    """
    try:
        bug_from_db = get_bug_by_id(session, bug_id)
        if not bug_from_db:
            raise HTTPException(status_code=404, detail=f"Bug with ID:{bug_id} not found!")

        bug_from_db.tags.clear()
        session.delete(bug_from_db)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Unable to DELETE Bug record with ID:{bug_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")