# tests/test_health_and_users.py
import allure
from config.settings import settings

@allure.feature("Environment & API Smoke")
@allure.story("Fetch Single Resource")
def test_get_post_by_id(api_client):
    assert settings.env in ["dev", "staging"]
    response = api_client.get("/posts/1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert "title" in body
