# ============================================================
# File: tests/conftest.py
# Description: Shared pytest fixtures for DB setup & JWT client
# ============================================================

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine
from backend.seed import run as seed_db  # ✅ import directly

# Base FastAPI test client
client = TestClient(app)

# ---------------------------
# DB Setup + Teardown
# ---------------------------
@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Drop & recreate DB, then seed data for tests."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Seed data directly
    seed_db(reset=False)

    yield
    Base.metadata.drop_all(bind=engine)


# ---------------------------
# JWT Authenticated Client
# ---------------------------
@pytest.fixture
def auth_client():
    """
    Returns a client with Authorization header set.
    Registers and logs in a default test user automatically.
    """
    # Register user
    client.post("/register", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpass"
    })

    # Login to get token
    res = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass"
    })
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Attach token to client headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
