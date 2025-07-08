import pytest
from app.models.bug import Bug
from app.schemas.bug import Status, Priority, Severity
from app.services.bug import sync_tags, get_bug_by_id
from app.services.helpers import Operation
from app.services.tag import get_all_tags

@pytest.mark.parametrize(
    ("bug_orm", "tags", "expected_tags", "expected_ids"),
    [
        (
            Bug(title="Title", description="desc", status=Status.OPEN, priority=Priority.HIGH,
                severity=Severity.CRITICAL, tags=[]),
            [], [], []
        ),
        (
            Bug(title="Title", description="desc", status=Status.OPEN, priority=Priority.HIGH,
                severity=Severity.CRITICAL, tags=[]),
            ["test", "tag"], ["test", "tag"], [1, 2]
        ),
        (
            Bug(title="Title", description="desc", status=Status.OPEN, priority=Priority.HIGH,
                severity=Severity.CRITICAL, tags=[]),
            ["test", "tag", "another", "new"], ["test", "tag", "another", "new"], [1, 2, 3, 4, 5]
        )
    ]
)
def test_sync_tags_create_new(session_client, bug_orm, tags, expected_tags, expected_ids):
    session_client.add(bug_orm)
    session_client.commit()

    bug_obj = get_bug_by_id(session_client, 1)
    sync_tags(session_client, bug_obj, tags)
    session_client.commit()


    created_tags = get_all_tags(session_client)
    assert all(tag.name in expected_tags for tag in created_tags)
    assert all(tag.id in expected_ids for tag in created_tags)
    assert len(created_tags) == len(expected_tags)

def run_sync_tags_test(session_client, operation, bug_orm, tags, expected_tags, expected_ids):
    session_client.add(bug_orm)
    session_client.commit()

    bug_obj = get_bug_by_id(session_client, 1)

    for _ in range(2):
        sync_tags(session_client, bug_obj, tags, operation)
        session_client.commit()

    all_tags = get_all_tags(session_client)
    assert len(all_tags) == len(expected_tags)
    assert all(tag.id in expected_ids for tag in all_tags)
    assert all(tag.name in expected_tags for tag in all_tags)

def test_sync_tags_create_duplicate(session_client):
    run_sync_tags_test(
        session_client,
        operation=Operation.CREATE,
        bug_orm=Bug(title="Title", description="desc", status=Status.OPEN, priority=Priority.HIGH,
                    severity=Severity.CRITICAL, tags=[]),
        tags=["tags", "create", "duplicate"],
        expected_tags=["tags", "create", "duplicate"],
        expected_ids=[1, 2, 3],
    )


def test_sync_tags_patch_duplicate(session_client):
    run_sync_tags_test(
        session_client,
        operation=Operation.PATCH,
        bug_orm=Bug(title="Title", description="desc", status=Status.OPEN, priority=Priority.HIGH,
                    severity=Severity.CRITICAL, tags=[]),
        tags=["tags", "patch", "duplicate"],
        expected_tags=["tags", "patch", "duplicate"],
        expected_ids=[1, 2, 3],
    )


def test_sync_tags_put_duplicate(session_client):
    run_sync_tags_test(
        session_client,
        operation=Operation.PUT,
        bug_orm=Bug(title="Title", description="desc", status=Status.OPEN, priority=Priority.HIGH,
                    severity=Severity.CRITICAL, tags=[]),
        tags=["tags", "put", "duplicate"],
        expected_tags=["tags", "put", "duplicate"],
        expected_ids=[1, 2, 3],
    )
