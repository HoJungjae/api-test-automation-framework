import pytest
import json
from utils.api_client import APIClient
from utils.validators import validate_keys


# All tests use the session-scoped api_client fixture from conftest.py


@pytest.mark.live
def test_get_posts(api_client):
    response = api_client.get("/posts")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    validate_keys(data[0], ["title", "body", "userId"])


@pytest.mark.live
def test_get_single_post(api_client):
    response = api_client.get("/posts/1")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert isinstance(data["title"], str)
    assert isinstance(data["userId"], int)


@pytest.mark.live
def test_invalid_post(api_client):
    response = api_client.get("/posts/99999", expect_failure=True)

    assert response.status_code in [200, 404]

    data = response.json()
    assert data == {} or isinstance(data, dict)


@pytest.mark.live
def test_create_post(api_client):
    payload = {
        "title": "test",
        "body": "test body",
        "userId": 1
    }

    response = api_client.post("/posts", payload)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]


def load_test_data():
    with open("data/test_data.json") as f:
        return json.load(f)


@pytest.mark.live
@pytest.mark.parametrize("case", load_test_data())
def test_post_user(api_client, case):
    response = api_client.get(f"/posts/{case['post_id']}")

    assert response.status_code == 200

    data = response.json()
    assert data["userId"] == case["expected_user"]
