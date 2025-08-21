# CRM/tests/test_payments.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# ---------- Helpers ----------
def create_user():
    res = client.post("/users/", json={
        "name": "Payment User",
        "email": "paymentuser@example.com",
        "password": "pass123"
    })
    assert res.status_code == 201
    return res.json()["id"]

def create_client():
    user_id = create_user()
    res = client.post("/clients/", json={
        "user_id": user_id,
        "name": "Payment Client",
        "email": "paymentclient@example.com",
        "phone": "1111111111"
    })
    assert res.status_code == 201
    return res.json()["id"]

def create_payment():
    client_id = create_client()
    res = client.post("/payments/", json={
        "client_id": client_id,
        "amount": 100.0,
        "status": "pending"
    })
    assert res.status_code == 201
    return res.json()["id"]

# ---------- Tests ----------
def test_create_payment():
    payment_id = create_payment()
    assert payment_id > 0

def test_list_payments():
    create_payment()
    res = client.get("/payments/")
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_update_payment():
    payment_id = create_payment()  # ✅ should return payment id
    res = client.put(f"/payments/{payment_id}", json={"status": "paid"})
    assert res.status_code == 200
    assert res.json()["status"] == "paid"



def test_delete_payment():
    payment_id = create_payment()
    res = client.delete(f"/payments/{payment_id}")
    assert res.status_code == 200
    assert "deleted" in res.json().get("message", "").lower()
