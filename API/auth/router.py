from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import getDB, verify_password, verify_telegram_auth
from . import schemas as s
from . import crud as c
from users.models import Users
from users import schemas as us
from users import crud as uc

router = APIRouter()

@router.get("/me", response_model=us.UserOut)
def me(db: Session = Depends(getDB), current_user: Users = Depends(c.get_current_user)):
    user = uc.get_user(db=db, id=current_user.id)
    return user

@router.post("/login", response_model=s.TokenPayload)
def login(data: us.UserCreate, db: Session = Depends(getDB)):
    if not verify_telegram_auth(data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Telegram credentials."
        )
    
    user = db.query(Users).filter(Users.telegram_id == data.telegram_id).first()

    if not user:
        user = uc.create_user(db=db, data=data)

        token = c.encode_token({"sub": str(user.id)})

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    
    if user:
        token = c.encode_token({"sub": str(user.id)})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

@router.put("/update", response_model=us.UserUpdate)
def update(data: us.UserUpdate, db: Session = Depends(getDB), current_user: Users = Depends(c.get_current_user)):
    if data.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action.."
        )
    user = uc.update_user(db, data)
    return user
