from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_payment():
    # Create user
    user_resp = client.post("/users/", json={
        "name": "Payment Owner",
        "email": "paymentowner@example.com",
        "password": "pass123"
    })
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    # Create client (✅ add phone!)
    client_resp = client.post("/clients/", json={
        "name": "Payment Client",
        "email": "paymentclient@example.com",
        "phone": "1234567890",  # ✅ fix
        "user_id": user_id
    })
    assert client_resp.status_code == 201
    client_id = client_resp.json()["id"]

    # Create payment
    payload = {
        "amount": 1500.00,
        "client_id": client_id
    }
    response = client.post("/payments/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == payload["amount"]
    assert data["client_id"] == client_id
    assert "id" in data
