from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:POSTGRES@localhost:5432/crm_db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1;"))
    print("✅ Connected to DB! Result:", result.scalar())
