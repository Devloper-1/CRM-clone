from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import database , models
import time

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Example stored user
USER_EMAIL = "test@example.com"
USER_PASSWORD_HASH = pwd_context.hash("123456")  # hashed version

# Store active tokens in memory
active_tokens = {}

class LoginData(BaseModel):
    email: str
    password: str
@router.post("/login")
def login(data: LoginData):
    # Check email
    if data.email != USER_EMAIL:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Check password (hashed)
    if not pwd_context.verify(data.password, USER_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate simple token
    token = f"{data.email}-{int(time.time())}"
    active_tokens[token] = True
    return {"token": token}

@router.post("/logout")
def logout(token: str):
    if token in active_tokens:
        del active_tokens[token]
        return {"message": "Logged out"}
    raise HTTPException(status_code=401, detail="Invalid token")
