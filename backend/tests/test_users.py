from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_user():
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "id" in data
