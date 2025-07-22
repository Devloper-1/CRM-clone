from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
 
#  URL of DATABASE 
DATABASE_URL = "postgresql+psycopg2://postgres:POSTGRES@localhost:5432/crm_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1;"))
    print("✅ Connected to DB! Result:", result.scalar())


