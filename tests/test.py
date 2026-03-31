from utils.api_client import APIClient

client = APIClient("https://jsonplaceholder.typicode.com")

response = client.get("/posts")
print(response.status_code)