import unittest
from unittest.mock import patch, MagicMock
from utils.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


class TestAPIClientMocked(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests in this class."""
        cls.client = APIClient(BASE_URL)

    def setUp(self):
        """Runs before each individual test."""
        pass

    @patch("utils.api_client.requests.get")
    def test_get_post_returns_200(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "title": "test title"}
        mock_get.return_value = mock_response

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
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 101, "title": "new"}
        mock_post.return_value = mock_response

        response = self.client.post("/posts", {"title": "new", "userId": 1})

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def tearDown(self):
        """Runs after each individual test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests in this class."""
        pass


if __name__ == "__main__":
    unittest.main()
