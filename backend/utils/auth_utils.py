# ============================================================
# File: backend/utils/auth_utils.py
# Description: JWT utilities (token creation & verification)
# ============================================================

# ============================================================
# Imports
# ============================================================
from fastapi import Header, HTTPException
from jose import JWTError , jwt
from datetime import datetime , timedelta
import os



# ----------------------------
# Secret key and algorithm
# ----------------------------
SECRET_KEY= os.getenv("SECRET_KEY" , "changeme_secret_key") # changeme_secret_key is if env fail to to send secret_key
AGORITHM= os.getenv("AGORITHM","HS256") 
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 ))


# ----------------------------
# Create JWT token
# ----------------------------
def create_access_token(data : dict , expire_delta : timedelta | None = None):
 """
    Create a signed JWT token.
    - data: payload dict (e.g. {"sub": user_email})
    - expires_delta: optional timedelta for custom expiration
    """
 to_encode = data.copy()
 expire = datetime.utcnow() + (expire_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
 to_encode.update({"exp":expire})
 return jwt.encode(to_encode,SECRET_KEY,algorithm=AGORITHM)

 
# ----------------------------
# Verify JWT token
# ----------------------------
def verify_token(authorization : str = Header(None)):
  """
    Verify the provided JWT token from the Authorization header.
    Example header: "Authorization: Bearer <token>"
    """
  if not authorization or not authorization.startswith("Bearer"):
    raise HTTPException(status_code=401 , detail="Missing or invalid Authorization header")
  token = authorization.split (" ")[1]
  try:
    payload = jwt.decode(token,SECRET_KEY,algorithms=[AGORITHM])
    return payload
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid or expired token")
  
