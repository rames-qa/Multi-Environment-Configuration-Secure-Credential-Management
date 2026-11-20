# tests/conftest.py
import pytest
from config.settings import settings
from core.http_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    headers = {}
    if settings.client_id:
        headers["X-Client-Id"] = settings.client_id
    client = APIClient(base_url=settings.base_url, headers=headers)
    yield client
    client.close()
