from pydantic import BaseModel, EmailStr
from typing import Optional

# ==========================
# 🚀 User Schemas
# ==========================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


# ==========================
# 🧰 Client Schemas
# ==========================

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str]
    user_id: int

class ClientUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    user_id: Optional[int]
    
class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    user_id: int

    model_config = {
        "from_attributes": True
    }


# ==========================
# 📋 Task Schemas
# ==========================

class TaskCreate(BaseModel):
    description: str
    status: Optional[str] = None
    client_id: int

class TaskUpdate(BaseModel):
    description: Optional[str]
    status: Optional[str]
    client_id: Optional[int]

class TaskResponse(BaseModel):
    id: int
    description: str
    status: str
    client_id: int

    class Config:
        orm_mode = True

 # ==========================
# 💰 Payment Schemas
# ==========================

class PaymentCreate(BaseModel):
    amount: float
    status: Optional[str] = None
    client_id: int

class PaymentUpdate(BaseModel):
    amount: Optional[float]
    status: Optional[str]
    client_id: Optional[int]

class PaymentResponse(BaseModel):
    id: int
    amount: float
    status: str
    client_id: int

    class Config:
        orm_mode = True
