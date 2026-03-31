import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response

    def post(self, endpoint, payload, headers=self.headers):
        response = requests.post(f"{self.base_url}{endpoint}", json=payload, headers=headers)
        response.raise_for_status()
        return response