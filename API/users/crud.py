from sqlalchemy.orm import Session
from . import schemas as s
from . import models as m
from fastapi import HTTPException, status
from dependencies import hash_password, verify_password
import uuid

def create_user(db: Session, data: s.UserCreate):
    try:
        user = db.query(m.Users).filter(
            m.Users.telegram_id == data.telegram_id
        ).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this telegram account already exists.",
            )
        user = db.query(m.Users).filter(
            m.Users.phone_number == data.phone_number
        ).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this phone number already exists.",
            )
        hashed_password = hash_password(data.password_hash)
        user_data = data.model_dump()
        user_data["password_hash"] = hashed_password
        user = m.Users(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def update_user(db: Session, data: s.UserUpdate):
    try:
        user = db.query(m.Users).filter(m.Users.id == data.id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not found."
            )
        for key, value in data.model_dump().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

def update_user_password(db: Session, data: s.UserPasswordUpdate):
    try:
        user = db.query(m.Users).filter(m.Users.id == data.id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not found."
            )
        if not verify_password(data.old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The password is incorrect."
            )
        user.password_hash = hash_password(data.new_password)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

def get_users(db: Session):
    try:
        return db.query(m.Users).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_user(db: Session, id: uuid.UUID):
    try:
        user = db.query(m.Users).filter(m.Users.id == id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not found."
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def delete_user(db: Session, id: uuid.UUID):
    try:
        user = get_user(db=db, id=id)
        db.delete(user)
        db.commit()
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
def deactivate_user(db: Session, id: uuid.UUID):
    try:
        user = get_user(db=db, id=id)
        user.is_active = False
        db.commit()
        db.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )