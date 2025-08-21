# Tests for Clients module
# CRM/tests/test_clients.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def create_user():
    res = client.post("/users/", json={
        "name": "Client User",
        "email": "clientuser@example.com",
        "password": "pass123"
    })
    assert res.status_code == 201
    return res.json()["id"]

def create_client():
    user_id = create_user()
    res = client.post("/clients/", json={
        "user_id": user_id,
        "name": "Test Client",
        "email": "client@example.com",
        "phone": "9999999999"
    })
    assert res.status_code == 201
    return res.json()["id"]

def test_create_client():
    client_id = create_client()
    assert client_id > 0

def test_list_clients():
    create_client()
    res = client.get("/clients/")
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_update_client():
    client_id = create_client()
    res = client.put(f"/clients/{client_id}", json={"name": "Updated Client"})
    assert res.status_code == 200
    assert res.json()["name"] == "Updated Client"

def test_delete_client():
    client_id = create_client()
    res = client.delete(f"/clients/{client_id}")
    assert res.status_code == 200
    assert "deleted" in res.json().get("message", "").lower()
