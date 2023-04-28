import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_signup_endpoint():
    # Test case for a valid new user registration
    new_user = {
        "Username": "fest@gmail.com ",
        "Password": "fest",
        "Name": "Test User",
        "Plan": "Basic",
        "AOI": ["art_gallery", "aquarium"]
    }
    response = await client.post("/signup", json=new_user)
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"
    assert response.json()["status_code"] == "200"

    # Test case for an already registered user
    response = await client.post("/signup", json=new_user)
    assert response.status_code == 404
    assert response.json()["message"] == "This email already exists"
    assert response.json()["status_code"]=="404"