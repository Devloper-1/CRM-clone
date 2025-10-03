# ============================================================
# File: backend/seed.py
# Description: Database seeder for dev & test environments
# ============================================================

from backend.database import SessionLocal, Base, engine
from backend.models import User, Client, Task, Payment

def run(reset: bool = False):
    """Seed the database with initial data."""
    db = SessionLocal()

    print("🔹 Ensuring tables exist...")
    Base.metadata.create_all(bind=engine)

    if reset:
        print("⚠️ Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Creating tables fresh...")
        Base.metadata.create_all(bind=engine)

    if not db.query(User).first():
        print("🔹 Inserting seed data...")

        # ----------------- USERS -----------------
        users = [
            User(name='Maheshwara', email='shadow_0@example.com', password='pass123'),
            User(name='Dark', email='shadow_1@example.com', password='pass123'),
            User(name='D', email='shadow_2@example.com', password='pass123'),
            User(name='O_G', email='shadow_3@example.com', password='pass123'),
        ]
        db.add_all(users)
        db.commit()

        # ----------------- CLIENTS -----------------
        clients = [
            Client(user_id=1, name='Maheshwara', email='shadow_0@example.com', phone='9999990000'),
            Client(user_id=1, name='Client 2', email='client2@example.com', phone='8888888888'),
            Client(user_id=1, name='Client 3', email='client3@example.com', phone='7777777777'),
            Client(user_id=2, name='Client 4', email='client4@example.com', phone='6666666666'),
            Client(user_id=2, name='Client 5', email='client5@example.com', phone='5555555555'),
            Client(user_id=2, name='Client 6', email='client6@example.com', phone='4444444444'),
            Client(user_id=1, name='Client 7', email='client7@example.com', phone='3333333333'),
            Client(user_id=1, name='Client 8', email='client8@example.com', phone='2222222222'),
            Client(user_id=2, name='Client 9', email='client9@example.com', phone='1111111111'),
            Client(user_id=2, name='Client 10', email='client10@example.com', phone='0000000000'),
        ]
        db.add_all(clients)
        db.commit()

        # ----------------- TASKS -----------------
        tasks = [
            Task(client_id=1, description='Follow up call', status='pending'),
            Task(client_id=2, description='Prepare invoice', status='completed'),
            Task(client_id=3, description='Send proposal', status='pending'),
            Task(client_id=4, description='Meeting with client', status='completed'),
            Task(client_id=5, description='Update CRM', status='pending'),
            Task(client_id=6, description='Payment reminder', status='pending'),
            Task(client_id=7, description='Draft contract', status='completed'),
            Task(client_id=8, description='Client onboarding', status='pending'),
            Task(client_id=9, description='Send feedback', status='completed'),
            Task(client_id=10, description='Schedule demo', status='pending'),
            Task(client_id=1, description='Check documents', status='completed'),
            Task(client_id=2, description='Follow up email', status='pending'),
            Task(client_id=3, description='Invoice verification', status='pending'),
            Task(client_id=4, description='Client satisfaction survey', status='completed'),
            Task(client_id=5, description='Prepare report', status='pending'),
        ]
        db.add_all(tasks)
        db.commit()

        # ----------------- PAYMENTS -----------------
        payments = [
            Payment(client_id=1, task_id=1, amount=500.00, status='pending'),
            Payment(client_id=2, task_id=2, amount=1000.00, status='paid'),
            Payment(client_id=3, task_id=3, amount=750.00, status='pending'),
            Payment(client_id=4, task_id=4, amount=1200.00, status='paid'),
            Payment(client_id=5, task_id=5, amount=650.00, status='pending'),
            Payment(client_id=6, task_id=6, amount=900.00, status='pending'),
            Payment(client_id=7, task_id=7, amount=1100.00, status='paid'),
            Payment(client_id=8, task_id=8, amount=400.00, status='pending'),
            Payment(client_id=9, task_id=9, amount=1300.00, status='paid'),
            Payment(client_id=10, task_id=10, amount=500.00, status='pending'),
            Payment(client_id=1, task_id=11, amount=600.00, status='paid'),
            Payment(client_id=2, task_id=12, amount=700.00, status='pending'),
            Payment(client_id=3, task_id=13, amount=800.00, status='pending'),
            Payment(client_id=4, task_id=14, amount=900.00, status='paid'),
            Payment(client_id=5, task_id=15, amount=1000.00, status='pending'),
        ]
        db.add_all(payments)
        db.commit()

        print("✅ Seed data inserted!")
    else:
        print("ℹ️ Database already has data. Skipping seeding.")

    db.close()
    print("🔍 Engine URL:", engine.url)
    print("🔍 Tables in metadata:", Base.metadata.tables.keys())


if __name__ == "__main__":
    choice = input("⚠️ Reset DB (drop all tables)? (y/N): ").strip().lower()
    run(reset=(choice == "y"))