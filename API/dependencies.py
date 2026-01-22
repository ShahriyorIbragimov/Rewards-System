from database import SessionLocal
from passlib.context import CryptContext
from fastapi import HTTPException, status
from users.models import Users, Role

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def isWho(user: Users, role: Role):
    if user.role == role:
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

