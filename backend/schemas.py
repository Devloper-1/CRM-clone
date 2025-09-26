# CRM/backend/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# ==================================================
# 🚀 USERS
# ==================================================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

# Login/Register schemas
class RegisterData(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginData(BaseModel):
    email: EmailStr
    password: str
# ==================================================
# 🧰 CLIENTS
# ==================================================

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    user_id: int

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    user_id: Optional[int] = None

class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# ==================================================
# 📋 TASKS
# ==================================================

class TaskCreate(BaseModel):
    description: str
    status: Optional[str] = "pending"  # ✅ prevents NULL error
    client_id: int

class TaskUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    client_id: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    description: str
    status: str
    client_id: int

    model_config = ConfigDict(from_attributes=True)


# ==================================================
# 💰 PAYMENTS
# ==================================================

class PaymentCreate(BaseModel):
    amount: float
    status: Optional[str] = "pending"
    client_id: int

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    status: Optional[str] = None
    client_id: Optional[int] = None

class PaymentResponse(BaseModel):
    id: int
    client_id: int
    task_id: Optional[int] = None
    amount: float
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
