from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend import models, database
from backend.schemas import UserCreate, UserUpdate, UserResponse
from backend.logging_config import logger

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserResponse])
def get_users(
    id: Optional[int] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.User)
    if id:
        query = query.filter(models.User.id == id)
    if email:
        query = query.filter(models.User.email == email)
    return query.all()

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User {db_user.id} created successfully")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email
    if user.password is not None:
        db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    logger.info(f"User {user_id} updated successfully")
    return db_user

@router.delete("/")
def delete_user(
    user_id: Optional[int] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.User)
    if user_id:
        db_user = query.filter(models.User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        return {"detail": f"User {user_id} deleted"}
    if email:
        deleted = query.filter(models.User.email == email).delete(synchronize_session=False)
        db.commit()
        return {"detail": f"{deleted} users deleted"}
    raise HTTPException(status_code=400, detail="Provide user_id or email for deletion")
