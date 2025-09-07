from jose import jwt, JWTError
from fastapi import HTTPException
from os import environ
from datetime import datetime, timezone, timedelta

SECRET_KEY: str = environ.get("SECRET_KEY") or ""
ALGORITHM: str = environ.get("ALGORITHM") or ""
EXPIRY: int = int(environ.get("EXPIRY") or 15)

print(SECRET_KEY, ALGORITHM)

def create_token(sub: str, expiry: int | None = None):
    
    if not expiry:
        expiry = EXPIRY
    
    to_encode = {"sub": sub, "exp": datetime.now(timezone.utc) + timedelta(minutes=expiry)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")