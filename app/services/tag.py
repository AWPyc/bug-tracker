import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.tag import Tag


def get_all_tags(session: Session):
    """
    Retrieve all tag records.

    Args:
        session (Session, optional): DB session.

    Returns:
        List[TagResponse]: List of all bugs or empty list if none exist.
    """
    try:
        tags_list_db = session.query(Tag).all()
        return tags_list_db
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Unable to fetch tags list!: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")