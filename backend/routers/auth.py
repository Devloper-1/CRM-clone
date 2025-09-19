from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import time
from backend import models
from backend.database import get_db
from backend.utils.auth_utils import active_tokens

router = APIRouter()

# bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =========================
# Schemas
# =========================
class RegisterData(BaseModel):
    name: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

# =========================
# Register
# =========================
@router.post("/register")
def register(data: RegisterData, db: Session = Depends(get_db)):
    # Check existing
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = pwd_context.hash(data.password)

    # Create user
    new_user = models.User(name=data.name, email=data.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}

# =========================
# Login
# =========================
@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = f"{data.email}-{int(time.time())}"
    active_tokens[token] = True
    return {"token": token}

# =========================
# Logout
# =========================
@router.post("/logout")
def logout(token: str):
    if token in active_tokens:
        del active_tokens[token]
        return {"message": "Logged out"}
    raise HTTPException(status_code=401, detail="Invalid token")
