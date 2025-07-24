# CRM/seed.py

from backend.database import SessionLocal
from backend.models import User, Client, Task, Payment

db = SessionLocal()

# Clear existing data
db.query(Payment).delete()
db.query(Task).delete()
db.query(Client).delete()
db.query(User).delete()
db.commit()

# 👤 Users
user1 = User(name="Admin", email="admin@example.com", password="admin123")
user2 = User(name="Staff", email="staff@example.com", password="staff123")
db.add_all([user1, user2])
db.commit()

db.refresh(user1)
db.refresh(user2)

# 👥 Clients (linked to user_id)
client1 = Client(name="Client A", email="a@x.com", phone="123", user_id=user1.id)
client2 = Client(name="Client B", email="b@x.com", phone="456", user_id=user1.id)
client3 = Client(name="Client C", email="c@x.com", phone="789", user_id=user2.id)
client4 = Client(name="Client D", email="d@x.com", phone="000", user_id=user2.id)
db.add_all([client1, client2, client3, client4])
db.commit()

db.refresh(client1)
db.refresh(client2)
db.refresh(client3)
db.refresh(client4)

# ✅ Tasks (only description + status, no title)
task1 = Task(description="Follow up with client", status="pending", client_id=client1.id)
task2 = Task(description="Gather documents", status="in_progress", client_id=client1.id)
task3 = Task(description="Design work", status="completed", client_id=client2.id)
task4 = Task(description="Initial meeting", status="pending", client_id=client3.id)
db.add_all([task1, task2, task3, task4])
db.commit()

# ✅ Payments (linked to clients)
payment1 = Payment(amount=1000, status="paid", client_id=client1.id)
payment2 = Payment(amount=1500, status="pending", client_id=client1.id)
payment3 = Payment(amount=1200, status="paid", client_id=client2.id)
payment4 = Payment(amount=1800, status="failed", client_id=client3.id)
db.add_all([payment1, payment2, payment3, payment4])
db.commit()

print("✅ Done: Users, Clients, Tasks, and Payments inserted.")
