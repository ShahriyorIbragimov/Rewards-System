from database import SessionLocal
from passlib.context import CryptContext
from fastapi import HTTPException, status
from users.models import Users, Role
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("API"))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_telegram_auth(data: dict):
    check_hash = data.pop("hash")
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))

    secret_key = hashlib.sha256(os.getenv("API").encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac_hash == check_hash

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def isAdmin(user: Users):
    if user.role == Role.admin:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not allowed to perform this action."
    )

def isActive(object):
    if object.is_active:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="This object is not active."
    )

