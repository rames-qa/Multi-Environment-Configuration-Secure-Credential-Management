# tests/conftest.py
import pytest
from config.settings import settings
from core.auth_manager import BearerTokenAuth
from core.http_client import APIClient
from clients.user_client import UserClient

@pytest.fixture(scope="session")
def api_client():
    auth = BearerTokenAuth(
        auth_url=settings.auth_url,
        client_id=settings.client_id,
        client_secret=settings.client_secret
    )
    client = APIClient(base_url=settings.base_url, auth=auth)
    yield client
    client.close()

@pytest.fixture(scope="session")
def user_client(api_client) -> UserClient:
    return UserClient(api_client)
