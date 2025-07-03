import time
import pytest
from datetime import datetime
from app.models.bug import Bug
from app.schemas.bug import BugCreate, Status, Priority, Severity, BugUpdate
from app.services.bug import get_bug_by_id
from app.services.helpers import apply_bug_data_to_model, assign_tags_to_bug, Operation
from tests.conftest import session_client

bug_create = BugCreate(
        title="Test title",
        description="Test desc",
        status=Status.OPEN,
        priority=Priority.HIGH,
        severity=Severity.CRITICAL,
        submitter="system",
        assigned_to="user_1",
        tags=[]
    )

bug_put = BugCreate(
        title="PUT title",
        description="PUT desc",
        status=Status.IN_PROGRESS,
        priority=Priority.MEDIUM,
        severity=Severity.MINOR,
        submitter="admin",
        assigned_to="user_2",
        tags=[]
    )

@pytest.mark.parametrize(
    ("bug_orm", "bug_create", "operation", "keys", "expected_values"),
    [
        (
            Bug(), bug_create, Operation.CREATE,
            ["title", "description", "status", "priority", "severity", "submitter", "assigned_to", "tags"],
            ["Test title", "Test desc", Status.OPEN, Priority.HIGH, Severity. CRITICAL, "system", "user_1", []]
         )
    ]
)
def test_apply_bug_data_to_model_success_create(session_client, bug_orm, bug_create, operation, keys, expected_values):
    apply_bug_data_to_model(bug_orm, bug_create, operation)

    session_client.add(bug_orm)
    session_client.commit()
    bug_obj = get_bug_by_id(session_client, 1)

    assert isinstance(bug_obj.created_at, datetime)
    assert isinstance(bug_obj.updated_at, datetime)

    delta = (bug_obj.updated_at - bug_obj.created_at).total_seconds()
    assert 0 <= delta <= 1

    for key, value in zip(keys, expected_values):
        assert bug_obj.__dict__[key] == value

@pytest.mark.parametrize(
    ("bug_orm", "bug_create", "operation", "bug_put", "keys", "expected_values"),
    [
        (
            Bug(), bug_create, Operation.PUT, bug_put,
            ["title", "description", "status", "priority", "severity", "submitter", "assigned_to", "tags"],
            ["PUT title", "PUT desc", Status.IN_PROGRESS, Priority.MEDIUM, Severity.MINOR, "admin", "user_2", []]
         )
    ]
)
def test_apply_bug_data_to_model_success_put(session_client, bug_orm, bug_create, operation, bug_put, keys,
                                             expected_values):
    apply_bug_data_to_model(bug_orm, bug_create, Operation.CREATE)

    session_client.add(bug_orm)
    session_client.commit()

    bug_obj = get_bug_by_id(session_client, 1)

    apply_bug_data_to_model(bug_obj, bug_put, operation)
    bug_obj = get_bug_by_id(session_client, 1)

    assert isinstance(bug_obj.created_at, datetime)
    assert isinstance(bug_obj.updated_at, datetime)

    delta = (bug_obj.updated_at - bug_obj.created_at).total_seconds()
    assert 0 <= delta <= 1

    for key, value in zip(keys, expected_values):
        assert bug_obj.__dict__[key] == value

@pytest.mark.parametrize(
    ("expected_key", "expected_value"),
    [
        ("title", "Title PATCH"),
        ("description", "Desc PATCH"),
        ("status", Status.CLOSED),
        ("priority", Priority.MEDIUM),
        ("severity", Severity.MINOR),
        ("submitter", "admin"),
        ("assigned_to", "user_2"),
        ("tags", [])
    ]
)
def test_apply_bug_data_to_model_success_patch(session_client, expected_key, expected_value):
    bug_orm = Bug()
    apply_bug_data_to_model(bug_orm, bug_create, Operation.CREATE)

    session_client.add(bug_orm)
    session_client.commit()

    bug_obj = get_bug_by_id(session_client, 1)
    updated_at = bug_obj.updated_at

    time.sleep(1)
    bug_update = BugUpdate.model_validate({expected_key: expected_value})
    apply_bug_data_to_model(bug_obj, bug_update, Operation.PATCH)

    bug_obj_patch = get_bug_by_id(session_client, 1)

    assert bug_obj_patch.__dict__[expected_key] == expected_value

    for key, value in bug_create.model_dump().items():
        if key != expected_key:
            assert bug_obj.__dict__[key] == value

    assert updated_at < bug_obj_patch.updated_at


def test_assign_tags_to_bug_create(session_client):
    ...

def test_assign_tags_to_bug_patch(session_client):
    ...

def test_assign_tags_to_bug_put(session_client):
    ...
