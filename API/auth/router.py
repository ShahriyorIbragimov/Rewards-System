from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import getDB
from . import schemas as s
import json
from urllib.parse import parse_qsl
from pydantic import ValidationError
from . import crud as c
from users.models import Users, Role
from users import schemas as us
from users import crud as uc
from students import crud as sc
from students import schemas as ss
from students import models as sm
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("/me", response_model=ss.StudentOutWithUser)
def me(db: Session = Depends(getDB), current_user: Users = Depends(c.get_current_user)):
    user = uc.get_user(db=db, id=current_user.id)
    if user.role == Role.admin:
        pass
    if user.role == Role.teacher:
        pass
    if user.role == Role.student:
        student = db.query(sm.StudentProfiles).filter(sm.StudentProfiles.user_id == current_user.id)
        return student

@router.post("/login", response_model=s.TokenPayload)
def login(payload: s.InitDataPayload, db: Session = Depends(getDB)):
    parsed = dict(parse_qsl(payload.init_data))
    if "user" in parsed:
        try:
            parsed["user"] = json.loads(parsed["user"])
        except Exception:
            pass
    try:
        tdata = s.TelegramInitData(**parsed)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    user = db.query(Users).filter(Users.telegram_id == tdata.user.id).first()

    if not user:
        user_data = tdata.user.model_dump()
        user_data["role"] = Role.student
        if tdata.user.username == os.getenv("ADMIN"):
            user_data["role"] = Role.admin
        user_data["telegram_id"] = user_data.pop("id")
        
        user_create_data = us.UserCreate(**user_data)
        user = uc.create_user(db=db, data=user_create_data)

        student_data = {
            "user_id": user.id,
            "avatar_url": user.photo_url,
            "bio": "",
            "is_active": True
        }

        sc.create_student(db=db, data=ss.StudentCreate(**student_data))

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
            detail="You are not allowed to perform this action."
        )
    user = uc.update_user(db, data)
    return user
