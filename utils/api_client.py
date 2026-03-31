import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def get(self, endpoint, expect_failure=False):
        response = requests.get(f"{self.base_url}{endpoint}")
        if not expect_failure:
            response.raise_for_status()
        return response

    def post(self, endpoint, payload, expect_failure=False):
        response = requests.post(f"{self.base_url}{endpoint}", json=payload, headers=self.headers)
        response.raise_for_status()
        return response