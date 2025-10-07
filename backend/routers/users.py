# ============================================================
# 📂 backend/routers/users.py
# Description: CRUD operations for users (JWT protected)
# ============================================================
from  fastapi import APIRouter, HTTPException, Depends, Body, Query
from sqlalchemy.orm import Session
from typing import Optional , List
from backend import models
from backend.schemas import UserCreate, UserUpdate, UserResponse, RegisterData, LoginData
from backend.database import get_db
from backend.utils.auth_utils import create_access_token, verify_token
from passlib.context import CryptContext
from datetime import timedelta
from fastapi.responses import StreamingResponse
import io
import csv


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(verify_token)]
      )

# bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


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

    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.email}, expires_delta=token_expires)

    return {"access_token": token, "token_type": "bearer"}


# ----------------------
# Get users (protected)
# ----------------------
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# ----------------------
# Update user (protected)
# ----------------------
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate = Body(...), db: Session = Depends(get_db)):
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
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User {user_id} deleted"}

# ================================
# 5️⃣ Export User to CSV
# ================================
@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    """Export all users as a CSV file """
    users = db.query(models.User).all()

    # Use Stringio (text buffer)
    buffer = io.StringIO()
    writer = csv.writer(buffer , lineterminator='\n')

    # write user rows
    for user in users :
        writer.writerow([
             user.id,
             user.name,
             user.email,
             user.password                  
             ])
    #  Convert text buffer to bytes
    buffer_bytes = io.BytesIO(buffer.getvalue().encode('utf-8'))
    buffer.close()

    return StreamingResponse(
        buffer_bytes,
        media_type="text/csv",
        headers={"Content-Disposition":"attachment ; filename=users.csv"}
    )
