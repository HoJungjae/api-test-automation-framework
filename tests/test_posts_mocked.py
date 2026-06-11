import pytest
from unittest.mock import patch
from utils.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


class FakeResponse:
    """Minimal stand-in for a requests.Response object."""

    def __init__(self, status_code, body):
        self.status_code = status_code
        self._body = body

    def json(self):
        return self._body

    def raise_for_status(self):
        pass


# --- unittest.mock style ---

@pytest.mark.mocked
@patch("utils.api_client.requests.get")
def test_get_post_mocked(mock_get):
    mock_get.return_value = FakeResponse(200, {
        "id": 1,
        "title": "mocked title",
        "body": "mocked body",
        "userId": 1
    })
    client = APIClient(BASE_URL)
    response = client.get("/posts/1")
    assert response.status_code == 200
    assert response.json()["title"] == "mocked title"
    mock_get.assert_called_once()


@pytest.mark.mocked
@patch("utils.api_client.requests.get")
def test_network_failure_raises(mock_get):
    mock_get.side_effect = ConnectionError("Network unreachable")
    client = APIClient(BASE_URL)
    with pytest.raises(ConnectionError):
        client.get("/posts/1")


@pytest.mark.mocked
@patch("utils.api_client.requests.post")
def test_create_post_mocked(mock_post):
    mock_post.return_value = FakeResponse(201, {"id": 101, "title": "new post"})
    client = APIClient(BASE_URL)
    response = client.post("/posts", {"title": "new post", "userId": 1})
    assert response.status_code == 201
    assert response.json()["id"] == 101
    mock_post.assert_called_once()


# --- pytest-mock style (mocker fixture) ---

@pytest.mark.mocked
def test_get_post_with_mocker(mocker, api_client):
    mock_get = mocker.patch("utils.api_client.requests.get")
    mock_get.return_value = FakeResponse(200, {"id": 1, "title": "mocker title"})
    response = api_client.get("/posts/1")
    assert response.json()["title"] == "mocker title"
    mock_get.assert_called_once()
