import requests
from utils.logger import get_logger

logger = get_logger()

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def get(self, endpoint, expect_failure=False):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to {url}")
        
        response = requests.get(url)
        
        logger.info(f"Response status: {response.status_code}")

        if not expect_failure:
            response.raise_for_status()
        
        return response

    def post(self, endpoint, payload, expect_failure=False):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to {url} with payload: {payload}")

        response = requests.post(url, json=payload, headers=self.headers)

        logger.info(f"Response status: {response.status_code}")

        if not expect_failure:
            response.raise_for_status()

        return response