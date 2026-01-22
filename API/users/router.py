import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import getDB, isWho
from typing import List
from . import schemas as s
from . import crud as c
from . import models as m
from auth.crud import get_current_user

router = APIRouter()

@router.get("/list-all", response_model=List[s.UserOut])
def list_all_users(db: Session = Depends(getDB), current_user: m.Users = Depends(get_current_user)):
    if isWho(current_user, m.Role.admin):
        users = c.get_users(db)
        return users

@router.get(f"/list/{id}", response_model=s.UserOut)
def list_one_user(id: uuid.UUID, db: Session = Depends(getDB), current_user: m.Users = Depends(get_current_user)):
    if isWho(current_user, m.Role.admin):
        user = c.get_user(id=id, db=db)
        return user

@router.post("/create", response_model=s.UserOut)
def create_user(data: s.UserCreate, db: Session = Depends(getDB), current_user: m.Users = Depends(get_current_user)):
    if isWho(current_user, m.Role.admin):
        user = c.create_user(db, data)
        return user

@router.put("/update-user", response_model=s.UserOut)
def update_user(data: s.UserUpdate, db: Session = Depends(getDB), current_user: m.Users = Depends(get_current_user)):
    if isWho(current_user, m.Role.admin):
        user = c.update_user(db, data)
        return user

@router.delete(f"/delete/{id}", response_model=s.UserOut)
def delete_user(id: uuid.UUID, db: Session = Depends(getDB), current_user: m.Users = Depends(get_current_user)):
    if isWho(current_user, m.Role.admin):
        user = c.delete_user(db=db, id=id)
        return user
