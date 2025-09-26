from fastapi import APIRouter, HTTPException, Depends, Body, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend import models
from backend.schemas import UserCreate, UserUpdate, UserResponse, RegisterData, LoginData
from backend.database import get_db
from backend.utils.auth_utils import active_tokens, verify_token
from passlib.context import CryptContext
import time

router = APIRouter(prefix="/users", tags=["Users"])

# bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------
# Register
# ----------------------
@router.post("/register", response_model=UserResponse)
def register(data: RegisterData, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(data.password)
    new_user = models.User(name=data.name, email=data.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ----------------------
# Login
# ----------------------
@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # simple in-memory token
    token = f"{user.email}-{int(time.time())}"
    active_tokens[token] = user.id
    return {"token": token}

# ----------------------
# Logout
# ----------------------
@router.post("/logout")
def logout(token: str):
    if token in active_tokens:
        del active_tokens[token]
        return {"message": "Logged out"}
    raise HTTPException(status_code=401, detail="Invalid token")

# ----------------------
# Get users (protected)
# ----------------------
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return db.query(models.User).all()

# ----------------------
# Update user (protected)
# ----------------------
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate = Body(...), db: Session = Depends(get_db), token: str = Depends(verify_token)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    data = user_update.model_dump(exclude_unset=True)
    if "password" in data:
        data["password"] = pwd_context.hash(data["password"])

    for key, value in data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# ----------------------
# Delete user (protected)
# ----------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User {user_id} deleted"}
