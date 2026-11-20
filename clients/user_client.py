# clients/user_client.py
import httpx
from core.http_client import APIClient

class UserClient:
    def __init__(self, api_client: APIClient):
        self.api = api_client

    def get_user(self, user_id: int) -> httpx.Response:
        return self.api.get(f"/users/{user_id}")

    def create_user(self, payload: dict) -> httpx.Response:
        return self.api.post("/users", json=payload)
