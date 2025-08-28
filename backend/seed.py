from backend.database import SessionLocal, Base, engine
from backend.models import User, Client, Task, Payment  # noqa: F401


db = SessionLocal()

print("🔹 Ensuring tables exist...")
Base.metadata.create_all(bind=engine)

choice = input("⚠️ Reset DB (drop all tables)? (y/N): ").strip().lower()
if choice == "y":
    print("⚠️ Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Creating tables fresh...")
    Base.metadata.create_all(bind=engine)

if not db.query(User).first():
    print("🔹 Inserting seed data...")

    users = [
        User(name='Test User 1', email='user1@example.com', password='pass123'),
        User(name='Test User 2', email='user2@example.com', password='pass123'),
    ]
    db.add_all(users)
    db.commit()

    clients = [
        Client(user_id=1, name='Test Client 1', email='client1@example.com', phone='9999999999'),
        Client(user_id=1, name='Test Client 2', email='client2@example.com', phone='8888888888'),
        Client(user_id=2, name='Test Client 3', email='client3@example.com', phone='7777777777'),
    ]
    db.add_all(clients)
    db.commit()

    tasks = [
        Task(client_id=1, description='Follow up call', status='pending'),
        Task(client_id=2, description='Prepare invoice', status='completed'),
    ]
    db.add_all(tasks)
    db.commit()

    payments = [
        Payment(client_id=1, task_id=1, amount=500.00, status='pending'),
        Payment(client_id=2, task_id=2, amount=1000.00, status='paid'),
    ]
    db.add_all(payments)
    db.commit()

    print("✅ Seed data inserted!")
else:
    print("ℹ️ Database already has data. Skipping seeding.")

db.close()

print("🔍 Engine URL:", engine.url)
print("🔍 Tables in metadata:", Base.metadata.tables.keys())


