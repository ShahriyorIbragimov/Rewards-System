from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import getDB, verify_password
from . import schemas as s
from . import crud as c
from users.models import Users

router = APIRouter()

@router.post("/login", response_model=s.TokenPayload)
def login(data: s.UserLogin, db: Session = Depends(getDB)):
    user = db.query(Users).filter(Users.phone_number == data.phone_number).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this phone number is not found."
        )
    
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User password is incorrect."
        )
    
    token = c.encode_token({"sub": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }