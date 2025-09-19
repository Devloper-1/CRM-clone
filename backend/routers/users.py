# ================================
# 📂 backend/routers/users.py
# ================================

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import Optional
from backend import models
from backend.schemas import UserCreate, UserUpdate, UserResponse
from backend.database import get_db
from backend.utils.auth_utils import verify_token

router = APIRouter(prefix="/users", tags=["Users"])

# ===============================
# Login Token
# ===============================

@router.get("/users")
def get_users(token: str= Depends(verify_token) , db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# ================================
# 1️⃣ Get Users
# ================================
@router.get("/", response_model=list[UserResponse])
def get_users(
    id: Optional[int] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Fetch all users or filter by ID / Email"""
    query = db.query(models.User)
    if id:
        query = query.filter(models.User.id == id)
    if email:
        query = query.filter(models.User.email == email)
    return query.all()


# ================================
# 2️⃣ Create User
# ================================
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # ✅ Check for duplicate email
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ================================
# 3️⃣ Update User by ID
# ================================
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """Update user details"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# ================================
# 4️⃣ Delete User by ID
# ================================
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by its ID"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": f"User {user_id} deleted"}
