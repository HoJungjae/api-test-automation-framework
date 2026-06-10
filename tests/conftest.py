import pytest
from utils.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_client():
    """Session-scoped API client — created once for the entire test run."""
    client = APIClient(BASE_URL)
    yield client
    # teardown: nothing to close for HTTP, but yield pattern is demonstrated
