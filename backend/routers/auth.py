from datetime import time
from backend import models, routers
from backend.database import get_db
from backend.login import LoginData
from fastapi import Depends, HTTPException
from pytest import Session


@routers.post("/register")
def register(data: RegisterData, db: Session = Depends(get_db)): # type: ignore
    # check if email exists
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(data.password) # type: ignore
    new_user = models.User(name=data.name, email=data.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "User registered"}

@routers.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not pwd_context.verify(data.password, user.password): # type: ignore
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = f"{data.email}-{int(time.time())}"
    active_tokens[token] = True # type: ignore
    return {"token": token}
