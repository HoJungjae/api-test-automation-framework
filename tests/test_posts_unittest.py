import unittest
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


class TestAPIClientMocked(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient(BASE_URL)

    def setUp(self):
        pass

    @patch("utils.api_client.requests.get")
    def test_get_post_returns_200(self, mock_get):
        mock_get.return_value = FakeResponse(200, {"id": 1, "title": "test title"})
        response = self.client.get("/posts/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)
        self.assertIsInstance(response.json()["title"], str)

    @patch("utils.api_client.requests.get")
    def test_connection_error_raised(self, mock_get):
        mock_get.side_effect = ConnectionError("Unreachable")
        with self.assertRaises(ConnectionError):
            self.client.get("/posts/1")

    @patch("utils.api_client.requests.post")
    def test_create_post_returns_201(self, mock_post):
        mock_post.return_value = FakeResponse(201, {"id": 101, "title": "new"})
        response = self.client.post("/posts", {"title": "new", "userId": 1})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
