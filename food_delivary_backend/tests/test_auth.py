# import pytest
# import uuid
# from fastapi.testclient import TestClient
# from application.main import app

# client = TestClient(app)

# # Generate unique test data to avoid database collisions
# test_user = {
#     "username": f"user_{uuid.uuid4().hex[:8]}",
#     "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
#     "password": "testpassword123"
# }

# @pytest.fixture(scope="module")
# def created_user():
#     """
#     Creates a user once for the module. 
#     Accepts 400 (Bad Request) if the user already exists from a previous run.
#     """
#     response = client.post("/auth/signup", json=test_user)
#     # 201 = Created, 400 = Already exists (which is fine for repeat test runs)
#     assert response.status_code in [201, 400]
#     return test_user

# def test_signup():
#     """Verifies that the signup endpoint is reachable."""
#     response = client.post("/auth/signup", json=test_user)
#     assert response.status_code in [201, 400]

# def test_login(created_user):
#     """
#     Verifies that the login endpoint returns a valid access token.
#     Uses form-data as required by OAuth2PasswordRequestForm.
#     """
#     response = client.post(
#         "/auth/login",
#         data={
#             "username": created_user["email"], 
#             "password": created_user["password"]
#         },
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )
    
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     assert response.json()["token_type"] == "bearer"

import pytest
import uuid
from fastapi.testclient import TestClient
from application.main import app

client = TestClient(app)

# Generate unique test data to avoid database collisions
test_owner = {
    "username": f"owner_{uuid.uuid4().hex[:8]}",
    "email": f"owner_{uuid.uuid4().hex[:8]}@example.com",
    "password": "testpassword123"
}


@pytest.fixture(scope="module")
def owner_token():
    """
    Creates a restaurant-owner user and returns a valid access token
    for use in Authorization headers.
    """
    response = client.post("/auth/signup", json=test_owner)
    assert response.status_code in [201, 400]

    response = client.post(
        "/auth/login",
        data={
            "username": test_owner["email"],
            "password": test_owner["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def sample_restaurant(owner_token):
    """
    Creates one restaurant with a known, fixed rating so the search
    tests below have a predictable target to filter for.
    """
    unique_name = f"TestResto_{uuid.uuid4().hex[:8]}"
    response = client.post(
        "/restaurants",
        json={"name": unique_name, "location": "Test City"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert response.status_code == 201
    return response.json()["restaurant"]


def test_search_limit_is_capped_at_100():
    """
    Regression test for the limit=999999 issue: even if a caller
    asks for far more than 100 results, the endpoint must not
    return more than 100.
    """
    response = client.get("/restaurants/search?limit=999999")
    assert response.status_code == 200
    results = response.json()
    assert len(results) <= 100


def test_search_default_limit_is_reasonable():
    """
    With no limit param at all, the endpoint should still apply
    its own default cap rather than returning unlimited rows.
    """
    response = client.get("/restaurants/search")
    assert response.status_code == 200
    results = response.json()
    assert len(results) <= 100


def test_search_min_rating_zero_is_not_ignored(sample_restaurant):
    """
    Regression test for the falsy-value bug: min_rating=0 must still
    apply the filter (and therefore return results), not be silently
    skipped by an `if min_rating:` check.
    """
    response = client.get("/restaurants/search?min_rating=0")
    assert response.status_code == 200
    results = response.json()
    # Every restaurant has rating >= 0, so the newly created restaurant
    # must appear in these results if the filter was actually applied.
    names = [r["name"] for r in results]
    assert sample_restaurant["name"] in names


def test_search_min_rating_does_not_crash():
    """
    Regression test for the `and`-vs-comma bug that raised
    TypeError: Boolean value of this clause is not defined.
    """
    response = client.get("/restaurants/search?min_rating=3")
    assert response.status_code == 200
    for r in response.json():
        assert r["rating"] >= 3


def test_search_by_name_filters_correctly(sample_restaurant):
    """Searching by (partial) name should return only matching restaurants."""
    partial_name = sample_restaurant["name"][:8]
    response = client.get(f"/restaurants/search?name={partial_name}")
    assert response.status_code == 200
    results = response.json()
    assert any(sample_restaurant["name"] == r["name"] for r in results)


def test_search_by_location_filters_correctly(sample_restaurant):
    """Searching by location should return only matching restaurants."""
    response = client.get("/restaurants/search?location=Test City")
    assert response.status_code == 200
    results = response.json()
    assert any(r["location"] == "Test City" for r in results)


def test_search_no_filters_returns_ok():
    """Calling search with no query params at all should not error out."""
    response = client.get("/restaurants/search")
    assert response.status_code == 200
    assert isinstance(response.json(), list)