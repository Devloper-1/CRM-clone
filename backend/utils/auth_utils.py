from fastapi import Header, HTTPException

# your global token storage
active_tokens = {}

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]  # get part after "Bearer"
    if token not in active_tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return token
