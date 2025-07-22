from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_client():
    # Create user
    user_resp = client.post("/users/", json={
        "name": "Client Owner",
        "email": "owner@example.com",
        "password": "pass123"
    })
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    # Create client
    payload = {
        "name": "Test Client",
        "email": "client@example.com",
        "phone": "1234567890",
        "user_id": user_id
    }
    response = client.post("/clients/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["user_id"] == payload["user_id"]
    assert "id" in data
