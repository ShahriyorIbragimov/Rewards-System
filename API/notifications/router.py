from fastapi import APIRouter, Depends
from . import crud as c
from . import schemas as s
from users import models as um
from dependencies import getDB, isWho
from sqlalchemy.orm import Session
from typing import List
import uuid
from auth.crud import get_current_user

router = APIRouter()

@router.get("/list-all", response_model=List[s.NotificationOut])
def list_all_notifications(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        notifications = c.get_notifications(db)
        return notifications

@router.get("/list-read", response_model=List[s.NotificationOut])
def list_read_notifications(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        notifications = c.get_read_notifications(db)
        return notifications

@router.get("/list-unread", response_model=List[s.NotificationOut])
def list_unread_notifications(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        notifications = c.get_unread_notifications(db)
        return notifications

@router.get(f"/list/{id}", response_model=s.NotificationOut)
def list_one_notification(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        notification = c.get_notification(id=id, db=db)
        return notification

@router.post("/create", response_model=s.NotificationOut)
def create_notification(data: s.NotificationCreate, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        notification = c.create_notification(db, data)
        return notification

@router.put("/update", response_model=s.NotificationOut)
def update_notification(data: s.NotificationUpdate, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        notification = c.update_notification(db, data)
        return notification

@router.delete(f"/delete/{id}", response_model=s.NotificationOut)
def delete_notification(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        notification = c.delete_notification(db=db, id=id)
        return notification
