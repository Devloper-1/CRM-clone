from backend.database import engine, Base
from backend import models  # 👈 make sure this import is here!

if __name__ == "__main__":
    print("Dropping all tables…")
    Base.metadata.drop_all(bind=engine)

    print("Creating all tables…")
    Base.metadata.create_all(bind=engine)

    print("✅ Database reset complete.")
