import os
import sys
from dotenv import load_dotenv
import pytest

print("✅ Loading test environment…")
os.environ["ENV"] = "test"
load_dotenv(".env.test")

# Make sure backend/ is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tests.reset_db import reset_test_db

@pytest.fixture(autouse=True)
def clean_test_db():
    reset_test_db()
    yield
