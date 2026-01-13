from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import getDB, verify_password
from . import schemas as s
from . import crud as c
from users.models import Users
from users.schemas import UserCreate, UserOut, UserUpdate, UserPasswordUpdate
from users import crud as uc
import uuid

router = APIRouter()

@router.get("/me", response_model=UserOut)
def me(db: Session = Depends(getDB), current_user: Users = Depends(c.get_current_user)):
    user = uc.get_user(db=db, id=current_user.id)
    return user

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
    
    token = c.encode_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(getDB)):
    user = db.query(Users).filter(Users.phone_number == data.phone_number).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone number already exists."
        )
    
    user = uc.create_user(db=db, data=data)

    return user

@router.put("/update", response_model=UserUpdate)
def update(data: UserUpdate, db: Session = Depends(getDB), current_user: Users = Depends(c.get_current_user)):
    if data.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action.."
        )
    user = uc.update_user(db, data)
    return user

@router.put("/update-password")
def update_password(data: UserPasswordUpdate, db: Session = Depends(getDB), current_user: Users = Depends(c.get_current_user)):
    if data.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this action.."
        )
    uc.update_user_password(db=db, data=data)
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Password updated successfully!"
    )

@router.put(f"/deactivate/{id}", response_model=s.UserOut)
def deactivate_user(id: uuid.UUID, db: Session = Depends(getDB), current_user: Users = Depends(c.get_current_user)):
    if id == current_user.id:
        user = uc.deactivate_user(db=db, id=id)
        return user