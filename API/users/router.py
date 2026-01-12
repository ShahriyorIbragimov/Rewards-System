import uuid
from fastapi import APIRouter, Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session
from dependencies import getDB
from typing import List
from . import schemas as s
from . import crud as c

router = APIRouter()

@router.get("/list-all", response_model=List[s.UserOut])
def list_all_users(db: Session = Depends(getDB)):
    users = c.get_users(db)
    return users

@router.get(f"/list/{id}", response_model=s.UserOut)
def list_one_user(id: uuid.UUID, db: Session = Depends(getDB)):
    user = c.get_user(id=id, db=db)
    return user

@router.post("/create", response_model=s.UserOut)
def create_user(data: s.UserCreate, db: Session = Depends(getDB)):
    user = c.create_user(db, data)
    return user

@router.put("/update-user", response_model=s.UserOut)
def update_user(data: s.UserUpdate, db: Session = Depends(getDB)):
    user = c.update_user(db, data)
    return user

@router.put("/update-password", response_model=s.UserOut)
def update_user_password(data: s.UserPasswordUpdate, db: Session = Depends(getDB)):
    user = c.update_user_password(db, data)
    return user

@router.delete(f"/delete/{id}", response_model=s.UserOut)
def update_user(id: uuid.UUID, db: Session = Depends(getDB)):
    user = c.delete(db=db, id=id)
    return user
