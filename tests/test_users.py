# Tests for Users module
# CRM\test\test_users.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def create_user(name="Temp User", email="temp@example.com"):
    res = client.post("/users/", json={
        "name": name,
        "email": email,
        "password": "pass123"
    })
    assert res.status_code == 201
    return res.json()["id"]

def test_create_user():
    user_id = create_user()
    assert user_id > 0

def test_list_users():
    create_user()
    res = client.get("/users/")
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_update_user():
    user_id = create_user()
    res = client.put(f"/users/{user_id}", json={"name": "Updated User"})
    assert res.status_code == 200
    assert res.json()["name"] == "Updated User"

def test_delete_user():
    user_id = create_user()
    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200
    assert "deleted" in res.json().get("message", "").lower()
