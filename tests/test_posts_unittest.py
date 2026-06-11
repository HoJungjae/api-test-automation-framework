import unittest
from unittest.mock import patch, MagicMock
from utils.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


class TestAPIClientMocked(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient(BASE_URL)

    def setUp(self):
        pass

    @patch("utils.api_client.requests.get")
    def test_get_post_returns_200(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": 1, "title": "test title"}
        mock_get.return_value.raise_for_status.return_value = None

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
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": 101, "title": "new"}
        mock_post.return_value.raise_for_status.return_value = None

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
