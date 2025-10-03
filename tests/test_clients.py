# ============================================================
# File: tests/test_clients.py
# Description: Client CRUD tests
# ============================================================

def create_client(auth_client, user_id=1, name="Temp Client"):
    res = auth_client.post("/clients/", json={
        "name": name,
        "email": f"{name.lower().replace(' ', '')}@example.com",
        "phone": "9999999999",
        "user_id": user_id
    })
    assert res.status_code == 201
    return res.json()["id"]  # ✅ matches ClientResponse schema


def test_create_client(auth_client):
    client_id = create_client(auth_client)
    assert client_id > 0


def test_list_clients(auth_client):
    create_client(auth_client)
    res = auth_client.get("/clients/")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_update_client(auth_client):
    client_id = create_client(auth_client)
    res = auth_client.put(f"/clients/{client_id}", json={"name": "Updated Client"})
    assert res.status_code == 200
    assert res.json()["name"] == "Updated Client"


def test_delete_client(auth_client):
    client_id = create_client(auth_client)
    res = auth_client.delete(f"/clients/{client_id}")
    assert res.status_code == 200
    assert "deleted" in res.json()["message"].lower()
