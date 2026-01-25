import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import getDB, isWho
from typing import List
from . import schemas as s
from . import crud as c
from users import models as um
from auth.crud import get_current_user

router = APIRouter()

@router.get("/validate", response_model=s.AdminOut)
def validate(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        admin = c.validate(db=db, data=s.AdminCreate(
            user_id=current_user.id,
            avatar_url=current_user.photo_url,
            bio="",
            is_active=True
        ))
        if admin:
            return admin