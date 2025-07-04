import sqlite3
import time
import pytest
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.bug import Bug
from app.models.tag import Tag
from app.schemas.bug import BugCreate, Status, Priority, Severity, BugUpdate
from app.services.bug import get_bug_by_id
from app.services.helpers import apply_bug_data_to_model, assign_tags_to_bug, Operation
from app.services.tag import get_all_tags
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

@pytest.mark.parametrize(
    ("initial_values", "expected_values"),
    [
        ([], []),
        ([Tag(name="One")], ["One"]),
        ([Tag(name="TWO"), Tag(name="tags")], ["TWO", "tags"]),
        ([Tag(name="Multiple"), Tag(name="tags"), Tag(name="assigned"), Tag(name="to"), Tag(name="bug")],
         ["Multiple", "tags", "assigned", "to", "bug"])
    ]
)
def test_assign_tags_to_bug_create(session_client, initial_values, expected_values):
    bug_orm = Bug()
    apply_bug_data_to_model(bug_orm, bug_create, Operation.CREATE)
    session_client.add(bug_orm)
    session_client.commit()

    bug_obj = get_bug_by_id(session_client, 1)
    assert bug_obj.tags == []

    assign_tags_to_bug(bug_obj, initial_values, Operation.CREATE)
    session_client.add(bug_obj)
    session_client.commit()

    bug_obj_after_assign_tags = get_bug_by_id(session_client, 1)
    assert all([isinstance(tag, Tag) for tag in bug_obj_after_assign_tags.tags])
    assert all(tag.name in expected_values for tag in bug_obj_after_assign_tags.tags)
    assert len(bug_obj_after_assign_tags.tags) == len(expected_values)

@pytest.mark.parametrize(
    ("initial_tags", "patch_tags", "expected_tags"),
    [
        (
            [], [Tag(name="first"), Tag(name="tag")], ["first", "tag"]
        ),
        (
            [Tag(name="initial"), Tag(name="tags")], [Tag(name="additional"), Tag(name="tags")],
            ["initial", "tags", "additional", "tags"]
        )
    ]
)
def test_assign_tags_to_bug_patch(session_client, initial_tags, patch_tags, expected_tags):
    bug_orm = Bug()
    apply_bug_data_to_model(bug_orm, bug_create, Operation.CREATE)
    assign_tags_to_bug(bug_orm, initial_tags, Operation.CREATE)
    session_client.add(bug_orm)
    session_client.commit()

    bug_obj = get_bug_by_id(session_client, 1)
    assert all([isinstance(tag, Tag) for tag in bug_obj.tags])
    assert len(bug_obj.tags) == len(initial_tags)

    initial_tags_expected = [tag.name for tag in initial_tags]
    assert all([tag.name in initial_tags_expected for tag in bug_obj.tags])

    assign_tags_to_bug(bug_obj, patch_tags, Operation.PATCH)
    bug_after_patch = get_bug_by_id(session_client, 1)
    assert all([isinstance(tag, Tag) for tag in bug_after_patch.tags])
    assert all([tag.name in expected_tags for tag in bug_after_patch.tags])
    assert len(bug_after_patch.tags) == len(expected_tags)

@pytest.mark.parametrize(
    ("initial_tags", "put_tags", "expected_tags"),
    [
        (
            [], [Tag(name="put"), Tag(name="tags")], ["put", "tags"]
        ),
        (
            [Tag(name="initial"), Tag(name="tags")], [Tag(name="put"), Tag(name="tag")], ["put", "tag"]
        )
    ]
)
def test_assign_tags_to_bug_put(session_client, initial_tags, put_tags, expected_tags):
    bug_orm = Bug()
    apply_bug_data_to_model(bug_orm, bug_create, Operation.CREATE)
    assign_tags_to_bug(bug_orm, initial_tags, Operation.CREATE)
    session_client.add(bug_orm)
    session_client.commit()

    bug_obj = get_bug_by_id(session_client, 1)
    initial_tags_name = {tag.name for tag in initial_tags}
    assert all([isinstance(tag, Tag) for tag in bug_obj.tags])
    assert all([tag.name in initial_tags_name for tag in bug_obj.tags])
    assert len(bug_obj.tags) == len(initial_tags)

    assign_tags_to_bug(bug_obj, put_tags, Operation.PUT)
    session_client.add(bug_obj)
    session_client.commit()

    bug_obj_after_put = get_bug_by_id(session_client, 1)
    assert all([isinstance(tag, Tag) for tag in bug_obj_after_put.tags])
    assert all([tag.name in expected_tags for tag in bug_obj_after_put.tags])
    assert len(bug_obj_after_put.tags) == len(expected_tags)
    assert all([tag.name not in initial_tags_name for tag in bug_obj_after_put.tags])

    existing_tags = get_all_tags(session_client)
    existing_tags_names = {tag.name for tag in existing_tags}
    final_tag_names = {tag.name for tag in bug_obj_after_put.tags}
    expected_tags_names = initial_tags_name | final_tag_names

    assert existing_tags_names == expected_tags_names