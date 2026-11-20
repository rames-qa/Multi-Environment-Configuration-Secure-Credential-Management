# tests/test_users.py
import allure
from models.user_models import UserResponse

@allure.feature("User Management")
@allure.story("Retrieve User Profile")
def test_get_user_schema_and_business_rules(user_client):
    response = user_client.get_user(user_id=1)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    user = UserResponse.model_validate(response.json())

    assert user.id == 1
    assert "@" in user.email
