from utils.api_client import APIClient
from utils.validators import validate_keys

BASE_URL = "https://jsonplaceholder.typicode.com"

client = APIClient(BASE_URL)


def test_get_posts():
    response = client.get("/posts")

    # Status code validation
    assert response.status_code == 200

    data = response.json()

    # Validate response type
    assert isinstance(data, list)

    # Validate structure
    # assert "title" in data[0]
    # assert "body" in data[0]
    # assert "userId" in data[0]
    # assert all(key in data[0] for key in ["title", "body", "userId"])
    validate_keys(data[0], ["title", "body", "userId"])

def test_get_single_post():
    response = client.get("/posts/1")

    assert response.status_code == 200

    data = response.json()

    # Validate exact data
    assert data["id"] == 1
    assert "title" in data


def test_invalid_post():
    response = client.get("/posts/99999")

    # This API sometimes returns empty object instead of 404
    assert response.status_code in [200, 404]

    data = response.json()

    # Handle both cases safely
    assert data == {} or isinstance(data, dict)

# Data Driven Testing

import pytest, json


def load_test_data():
    with open("data/test_data.json") as f:
        return json.load(f)

# This is cool. Awesome concept. Super scalable.
@pytest.mark.parametrize("case", load_test_data())
def test_post_user(case):
    response = client.get(f"/posts/{case['post_id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["userId"] == case["expected_user"]