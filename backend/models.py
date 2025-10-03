# ============================================================
# File: backend/models.py
# Description: SQLAlchemy ORM models for Users, Clients, Tasks, and Payments
# ============================================================
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    clients = relationship("Client", back_populates="user", cascade="all, delete")

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)   # ✅ fixed

    user = relationship("User", back_populates="clients")
    tasks = relationship("Task", back_populates="client", cascade="all, delete")
    payments = relationship("Payment", back_populates="client", cascade="all, delete")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)

    # Relationships
    client = relationship("Client", back_populates="tasks")
    payments = relationship("Payment", back_populates="task", cascade="all, delete")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)

    amount = Column(Float, nullable=False)
    status = Column(String, default="pending", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    client = relationship("Client", back_populates="payments")
    task = relationship("Task", back_populates="payments")
