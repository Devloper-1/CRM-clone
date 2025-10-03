# ============================================================
# File: tests/test_users.py
# Description: User CRUD tests (JWT-protected)
# ============================================================

def create_user(auth_client, name="Temp User", email="temp@example.com"):
    res = auth_client.post("/register", json={
        "name": name,
        "email": email,
        "password": "pass123"
    })
    assert res.status_code == 200
    return res.json()["user_id"]  # ✅ matches auth.py


def test_create_user(auth_client):
    user_id = create_user(auth_client)
    assert user_id > 0


def test_list_users(auth_client):
    create_user(auth_client)
    res = auth_client.get("/users/")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_update_user(auth_client):
    user_id = create_user(auth_client)
    res = auth_client.put(f"/users/{user_id}", json={"name": "Updated User"})
    assert res.status_code == 200
    assert res.json()["name"] == "Updated User"


def test_delete_user(auth_client):
    user_id = create_user(auth_client)
    res = auth_client.delete(f"/users/{user_id}")
    assert res.status_code == 200
    assert "deleted" in res.json()["message"].lower()
