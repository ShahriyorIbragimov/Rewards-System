import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import getDB, isAdmin
from typing import List
from . import schemas as s
from . import crud as c
from . import models as m
from auth.crud import get_current_user

router = APIRouter()

@router.get("/list-all", response_model=List[s.RewardOut])
def list_all_rewards(group_id: uuid.UUID, db: Session = Depends(getDB), current_user: m.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        users = c.get_rewards(db=db, group_id=group_id)
        return users

@router.get(f"/list/{id}", response_model=s.RewardOut)
def list_one_reward(id: uuid.UUID, db: Session = Depends(getDB), current_user: m.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        reward = c.get_reward(id=id, db=db)
        return reward

@router.post("/create", response_model=s.RewardOut)
def create_reward(data: s.RewardCreate, db: Session = Depends(getDB), current_user: m.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        reward = c.create_reward(db, data)
        return reward

@router.delete(f"/delete/{id}", response_model=s.RewardOut)
def delete_reward(id: uuid.UUID, db: Session = Depends(getDB), current_user: m.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        reward = c.delete_reward(db=db, id=id)
        return reward
