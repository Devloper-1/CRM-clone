# ============================================================
# File: backend/routers/auth.py
# Description: Auth routes (register, login, logout)
# ============================================================

# ============================================================
# Import 
# ============================================================
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import timedelta
from backend import models
from backend.database import get_db
from backend.utils.auth_utils import  create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES


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

    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.email }, expire_delta=token_expires)
    
    # Returning both "token" (legacy) and "access_token" (standard)
    return {"access_token": token, "token_type": "bearer", "token": token}

# =========================
# Logout
# =========================
@router.post("/logout")
def logout():
    """
    JWT is stateless → Logout = client deletes token.
    """
    return {"message": "Logout successful (delete token on client side)"}
