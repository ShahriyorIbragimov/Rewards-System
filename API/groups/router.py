from fastapi import APIRouter, Depends
from . import crud as c
from . import schemas as s
from users import models as um
from dependencies import getDB, isAdmin
from sqlalchemy.orm import Session
from typing import List
import uuid
from auth.crud import get_current_user

router = APIRouter()

@router.get("/list-all", response_model=List[s.GroupOut])
def list_all_groups(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        groups = c.get_groups(db)
        return groups

@router.get("/list-active", response_model=List[s.GroupOut])
def list_active_groups(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        groups = c.get_active_groups(db)
        return groups
    
@router.get("/list-inactive", response_model=List[s.GroupOut])
def list_inactive_groups(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        groups = c.get_inactive_groups(db)
        return groups

@router.get(f"/list/{id}", response_model=s.GroupOut)
def list_one_group(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        group = c.get_group(id=id, db=db)
        return group

@router.post("/create", response_model=s.GroupOut)
def create_group(data: s.GroupCreate, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        group = c.create_group(db, data)
        return group

@router.put("/update", response_model=s.GroupOut)
def update_group(data: s.GroupUpdate, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        group = c.update_group(db, data)
        return group

@router.put(f"/deactivate/{id}", response_model=s.GroupOut)
def deactivate_group(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        group = c.deactivate_group(db=db, id=id)
        return group

@router.delete(f"/delete/{id}", response_model=s.GroupOut)
def delete_group(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        group = c.delete_group(db=db, id=id)
        return group

@router.get("/list-all", response_model=List[s.MemberOut])
def list_all_members(group_id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        members = c.get_members(db=db, group_id=group_id)
        return members

@router.get(f"/list/{id}", response_model=s.MemberOut)
def list_one_member(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        member = c.get_member(id=id, db=db)
        return member

@router.post("/add", response_model=s.MemberOut)
def add_member(data: s.MemberCreate, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        member = c.add_member(db, data)
        return member

@router.delete(f"/delete/{id}", response_model=s.MemberOut)
def delete_member(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isAdmin(current_user):
        member = c.delete_member(db=db, id=id)
        return member

