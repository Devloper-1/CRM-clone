from backend import models
from backend.database import engine, Base
import os
from dotenv import load_dotenv

# Load .env.test to get test DB URL
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, "tests", ".env.test")
load_dotenv(dotenv_path)

def reset_test_db():
    print("🔄 Resetting test database…")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Test database reset complete.")

if __name__ == "__main__":
    reset_test_db()
