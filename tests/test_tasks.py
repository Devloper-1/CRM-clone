# CRM/tests/test_tasks.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def create_user():
    res = client.post("/users/", json={
        "name": "Task User",
        "email": "taskuser@example.com",
        "password": "pass123"
    })
    assert res.status_code == 201
    return res.json()["id"]

def create_client():
    user_id = create_user()
    res = client.post("/clients/", json={
        "user_id": user_id,
        "name": "Task Client",
        "email": "taskclient@example.com",
        "phone": "1111111111"
    })
    assert res.status_code == 201
    return res.json()["id"]

def create_task():
    client_id = create_client()
    res = client.post("/tasks/", json={
        "client_id": client_id,
        "description": "Testing task creation",
        "status": "pending"  # ✅ Required
    })
    assert res.status_code == 201
    return res.json()["id"]

def test_create_task():
    task_id = create_task()
    assert task_id > 0

def test_list_tasks():
    create_task()
    res = client.get("/tasks/")
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_update_task():
    task_id = create_task()
    res = client.put(f"/tasks/{task_id}", json={"description": "Updated Task"})
    print("DEBUG:", res.status_code, res.json())  # ✅ Shows error if fails
    assert res.status_code == 200
    assert res.json()["description"] == "Updated Task"



def test_delete_task():
    task_id = create_task()
    res = client.delete(f"/tasks/{task_id}")
    assert res.status_code == 200
    assert "deleted" in res.json().get("message", "").lower()
