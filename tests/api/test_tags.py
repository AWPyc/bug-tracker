from tests.conftest import client
from tests.api.test_bugs import bug_create

def test_get_all_tags(client):
    response_get = client.get("/tags")
    assert response_get.status_code == 200

def test_tag_duplicate(client):
    bug_create.tags = ["test"]

    for _ in range(0, 2):
        response_post = client.post("/bugs", json=bug_create.model_dump())
        assert response_post.status_code == 201

    request_get = client.get("/tags")
    assert request_get.status_code == 200

    tag_data = request_get.json()
    assert len(tag_data) == 1
    assert any(tag["name"] == "test" for tag in tag_data)
