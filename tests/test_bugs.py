import pytest
from app.schemas.bug import Status, Priority, Severity, BugCreate, BugUpdate
from tests.conftest import client

bug_create = BugCreate(
        title="Test title",
        description="Test description",
        status=Status.OPEN,
        priority=Priority.HIGH,
        severity=Severity.CRITICAL,
        submitter="system",
        assigned_to=None,
        tags=["test", "tag"]
    )

def test_get_all_bugs_empty(client):
    response = client.get("/bugs")
    assert response.status_code == 200
    assert response.json() == []

def test_get_bug_by_id_empty(client):
    response = client.get("/bug/1")
    assert response.status_code == 404

@pytest.mark.parametrize("bug_create", [bug_create])
def test_post_bug_successful(client, bug_create):
    response = client.post("/bugs", json=bug_create.model_dump())
    assert response.status_code == 201

@pytest.mark.parametrize("bug_create", [bug_create])
def test_post_multiple_bug_same_data(client, bug_create):
    for _ in range(0,2):
        response = client.post("/bugs", json=bug_create.model_dump())
        assert response.status_code == 201

    response_get_1 = client.get("/bug/1")
    assert response_get_1.status_code == 200

    response_get_2 = client.get("/bug/2")
    assert response_get_2.status_code == 200

    response_check_1 = response_get_1.json()
    response_check_2 = response_get_2.json()

    assert response_check_1["id"] == 1
    assert response_check_2["id"] == 2
    assert response_check_1 is not response_check_2

def test_post_bug_unsuccessful(client):
    response = client.post("/bugs", json={})
    assert response.status_code == 422

@pytest.mark.parametrize("bug_create", [bug_create])
def test_get_bug_by_id(client, bug_create):
    response_post = client.post("/bugs", json=bug_create.model_dump())
    assert response_post.status_code == 201
    response_get = client.get("bug/1")
    assert response_get.status_code == 200

@pytest.mark.parametrize(
    ("bug_create", "bug_update", "expected_key", "expected_value"),
    [
        (bug_create, BugUpdate.model_validate({"title": "New title"}), "title", "New title"),
        (bug_create, BugUpdate.model_validate({"description": "New desc"}), "description", "New desc"),
        (bug_create, BugUpdate.model_validate({"status": Status.CLOSED}), "status", Status.CLOSED.value),
        (bug_create, BugUpdate.model_validate({"priority": Priority.LOW}), "priority", Priority.LOW),
        (bug_create, BugUpdate.model_validate({"severity": Severity.MINOR}), "severity", Severity.MINOR),
        (bug_create, BugUpdate.model_validate({"submitter": "user1"}), "submitter", "user1"),
        (bug_create, BugUpdate.model_validate({"assigned_to": "user2"}), "assigned_to", "user2")
    ]
)
def test_patch_one_field_successful(client, bug_create, bug_update, expected_key, expected_value):
    response_post = client.post("/bugs", json=bug_create.model_dump())
    assert response_post.status_code == 201

    response_patch = client.patch("/bug/1", json=bug_update.model_dump(exclude_unset=True))
    assert response_patch.status_code == 204

    response_check = client.get("/bug/1")
    assert response_check.status_code == 200

    bug_data = response_check.json()

    assert bug_data[expected_key] == expected_value

@pytest.mark.parametrize(
    ("bug_create", "bug_update", "expected_values"),
    [
        (bug_create, BugUpdate.model_validate({"tags": ["new", "another"]}), ["new","test","tag","another"])
    ]
)
def test_patch_only_tags_successful(client, bug_create, bug_update, expected_values):
    response_post = client.post("/bugs", json=bug_create.model_dump())
    assert response_post.status_code == 201

    bug_update = BugUpdate.model_validate({"tags": ["new", "another"]})

    response_patch = client.patch("/bug/1", json=bug_update.model_dump(exclude_unset=True))
    assert response_patch.status_code == 204

    response_check = client.get("/bug/1")

    bug_data = response_check.json()
    set_tags_names = {tag["name"] for tag in bug_data["tags"]}

    assert all(name in set_tags_names for name in expected_values)

@pytest.mark.parametrize(
    ("bug_create", "bugPut", "expected_keys", "expected_values"),
    [
        (
            bug_create, BugCreate(
            title="Title PUT",
            description="Desc PUT",
            status=Status.IN_PROGRESS,
            priority=Priority.MEDIUM,
            severity=Severity.MAJOR,
            submitter="admin",
            assigned_to="user_3",
            tags=["tags", "after", "PUT"]
            ),
            ["title", "description", "status", "priority", "severity", "submitter", "assigned_to", "tags"],
            ["Title PUT", "Desc PUT", Status.IN_PROGRESS, Priority.MEDIUM, Severity.MAJOR, "admin", "user_3", ["tags", "after", "PUT"]]
        )
    ]
)
def test_put_successful(client, bug_create, bugPut, expected_keys, expected_values):
    response_post = client.post("/bugs", json=bug_create.model_dump())
    assert response_post.status_code == 201

    response_put = client.put("/bug/1", json=bugPut.model_dump())
    assert response_put.status_code == 200

    response_check = client.get("/bug/1")
    assert response_check.status_code == 200

    bug_data = response_check.json()

    for key, expected in zip(expected_keys, expected_values):
        actual = bug_data[key]
        if isinstance(actual, list):
            set_tags_names = {tag["name"] for tag in bug_data["tags"]}
            assert all(name in set_tags_names for name in expected)
        else:
            assert actual == expected

def test_put_unsuccessful(client):
    response_get = client.get("/bug/1")
    assert response_get.status_code == 404
    response_put = client.put("/bug/1", json=bug_create.model_dump())
    assert response_put.status_code == 404

@pytest.mark.parametrize("bug_create", [bug_create])
def test_delete_bug_successful(client, bug_create):
    response_post = client.post("/bugs", json=bug_create.model_dump())
    assert response_post.status_code == 201
    response_get = client.get("/bug/1")
    assert response_get.status_code == 200
    response_delete = client.delete("/bug/1")
    assert response_delete.status_code == 204

def test_delete_bug_unsuccessful(client):
    response_delete = client.delete("/bug/1")
    assert response_delete.status_code == 404

