import pytest
from pydantic import ValidationError

from app.schemas.bug import BugCreate, Status, Priority, Severity


def test_create_bug_valid():
    bug = BugCreate(
        title='Invalid API response',
        description='Creating bug record ends in Internal Server Error [500]',
        status=Status.OPEN,
        priority=Priority.HIGH,
        severity=Severity.CRITICAL,
        assigned_to=None,
        tags=None,
        submitter=None
    )
    assert bug.title == 'Invalid API response'
    assert bug.description == 'Creating bug record ends in Internal Server Error [500]'
    assert bug.status == Status.OPEN
    assert bug.priority == Priority.HIGH
    assert bug.severity == Severity.CRITICAL
    assert bug.assigned_to is None
    assert bug.tags is None
    assert bug.submitter is None

def test_create_bug_invalid_empty_title():
    with pytest.raises(ValidationError):
        BugCreate(
        title='',
        description='Valid desc',
        status=Status.OPEN,
        priority=Priority.HIGH,
        severity=Severity.CRITICAL,
        assigned_to=None,
        tags=None,
        submitter=None
    )

def test_create_bug_invalid_whitespace_title():
    with pytest.raises(ValidationError):
        BugCreate(
        title='           ',
        description='Valid desc',
        status=Status.OPEN,
        priority=Priority.HIGH,
        severity=Severity.CRITICAL,
        assigned_to=None,
        tags=None,
        submitter=None
        )