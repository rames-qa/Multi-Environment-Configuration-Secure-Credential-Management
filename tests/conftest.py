import pytest
from config.settings import settings
from core.http_client import APIClient
from clients.user_client import UserClient
@pytest.fixture(scope="session")
def api_client():
    headers = {}

    if settings.client_id:
        headers["X-Client-Id"] = settings.client_id

    client = APIClient(
        base_url=settings.base_url,
        headers=headers
    )

    yield client
    client.close()
@pytest.fixture(scope="session")
def user_client(api_client):
    return UserClient(api_client)
