import pytest
import uuid
from fastapi.testclient import TestClient
from application.main import app

client = TestClient(app)

# Generate unique test data to avoid database collisions
test_user = {
    "username": f"user_{uuid.uuid4().hex[:8]}",
    "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
    "password": "testpassword123"
}

@pytest.fixture(scope="module")
def created_user():
    """
    Creates a user once for the module. 
    Accepts 400 (Bad Request) if the user already exists from a previous run.
    """
    response = client.post("/auth/signup", json=test_user)
    # 201 = Created, 400 = Already exists (which is fine for repeat test runs)
    assert response.status_code in [201, 400]
    return test_user

def test_signup():
    """Verifies that the signup endpoint is reachable."""
    response = client.post("/auth/signup", json=test_user)
    assert response.status_code in [201, 400]

def test_login(created_user):
    """
    Verifies that the login endpoint returns a valid access token.
    Uses form-data as required by OAuth2PasswordRequestForm.
    """
    response = client.post(
        "/auth/login",
        data={
            "username": created_user["email"], 
            "password": created_user["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"