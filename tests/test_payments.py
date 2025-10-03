# ============================================================
# File: tests/test_payments.py
# Description: Payment CRUD tests (JWT-protected)
# ============================================================

def create_payment(auth_client, client_id=1, task_id=None, amount=100.0):
    res = auth_client.post("/payments/", json={
        "amount": amount,
        "status": "pending",
        "client_id": client_id,
        "task_id": task_id
    })
    assert res.status_code == 201
    return res.json()["id"]  # ✅ matches PaymentResponse


def test_create_payment(auth_client):
    payment_id = create_payment(auth_client)
    assert payment_id > 0


def test_list_payments(auth_client):
    create_payment(auth_client)
    res = auth_client.get("/payments/")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_update_payment(auth_client):
    payment_id = create_payment(auth_client)
    res = auth_client.put(f"/payments/{payment_id}", json={"status": "paid"})
    assert res.status_code == 200
    assert res.json()["status"] == "paid"


def test_delete_payment(auth_client):
    payment_id = create_payment(auth_client)
    res = auth_client.delete(f"/payments/{payment_id}")
    assert res.status_code == 200
    assert "deleted" in res.json()["message"].lower()
