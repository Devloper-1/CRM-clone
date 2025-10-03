# ============================================================
# File: tests/test_tasks.py
# Description: Task CRUD tests (JWT-protected)
# ============================================================

def create_task(auth_client, client_id=1, description="Temp Task"):
    res = auth_client.post("/tasks/", json={
        "description": description,
        "status": "pending",
        "client_id": client_id
    })
    assert res.status_code == 201
    return res.json()["id"]  # ✅ matches TaskResponse


def test_create_task(auth_client):
    task_id = create_task(auth_client)
    assert task_id > 0


def test_list_tasks(auth_client):
    create_task(auth_client)
    res = auth_client.get("/tasks/")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_update_task(auth_client):
    task_id = create_task(auth_client)
    res = auth_client.put(f"/tasks/{task_id}", json={"description": "Updated Task"})
    assert res.status_code == 200
    assert res.json()["description"] == "Updated Task"


def test_delete_task(auth_client):
    task_id = create_task(auth_client)
    res = auth_client.delete(f"/tasks/{task_id}")
    assert res.status_code == 200
    assert "deleted" in res.json()["message"].lower()
