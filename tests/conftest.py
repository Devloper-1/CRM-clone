# CRM/tests/conftest.py
import pytest
import subprocess
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine

client = TestClient(app)

def pytest_addoption(parser):
    parser.addoption("--seed", action="store_true", help="Seed the database before tests")

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db(request):
    """Clean DB before & after each test; optionally seed."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    if request.config.getoption("--seed"):
        print("🌱 Seeding database with sample data...")
        subprocess.run(["python", "backend/seed.py"], check=True)

    yield

    Base.metadata.drop_all(bind=engine)
