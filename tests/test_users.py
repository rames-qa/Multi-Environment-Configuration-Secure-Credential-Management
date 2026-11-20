# tests/test_users.py
import allure
from models.user_models import UserResponse

@allure.feature("User Management")
@allure.story("Retrieve User Profile")
def test_get_user_schema_and_business_rules(user_client):
    response = user_client.get_user(user_id=1)

    # 1. Status Assertion
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # 2. Schema Validation (Pydantic raises ValidationError if types/fields fail)
    user = UserResponse.model_validate(response.json())

    # 3. Business Rule Assertion
    assert user.id == 1
    assert user.role in ["admin", "member"]
