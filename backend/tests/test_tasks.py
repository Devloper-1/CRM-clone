from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_task():
    # Create user
    user_resp = client.post("/users/", json={
        "name": "Task Owner",
        "email": "taskowner@example.com",
        "password": "pass123"
    })
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    # Create client
    client_resp = client.post("/clients/", json={
        "name": "Task Client",
        "email": "taskclient@example.com",
        "phone": "1234567890",
        "user_id": user_id
    })
    assert client_resp.status_code == 201
    client_id = client_resp.json()["id"]

    # Create task
    payload = {
        "description": "This is a test task",
        "status": "pending",   # ✅ required in your DB
        "client_id": client_id
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == payload["description"]
    assert data["status"] == payload["status"]
    assert data["client_id"] == client_id
    assert "id" in data
