# ============================================================
# File: tests/test_auth.py
# Description: Test JWT-auth and registration/login
# ============================================================

def test_register_success(auth_client):
    res = auth_client.post("/register", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "pass123"
    })
    assert res.status_code == 200
    assert "user_id" in res.json()


def test_register_duplicate_email(auth_client):
    # First registration
    auth_client.post("/register", json={
        "name": "Bob",
        "email": "bob@example.com",
        "password": "pass123"
    })
    # Duplicate
    res = auth_client.post("/register", json={
        "name": "Bob2",
        "email": "bob@example.com",
        "password": "pass123"
    })
    assert res.status_code == 400


def test_login_success(auth_client):
    auth_client.post("/register", json={
        "name": "Charlie",
        "email": "charlie@example.com",
        "password": "pass123"
    })
    res = auth_client.post("/login", json={
        "email": "charlie@example.com",
        "password": "pass123"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_protected_route_requires_jwt():
    from fastapi.testclient import TestClient
    from backend.main import app
    client = TestClient(app)
    res = client.get("/users/")
    assert res.status_code == 401


def test_protected_route_with_jwt(auth_client):
    res = auth_client.get("/users/")
    assert res.status_code == 200
