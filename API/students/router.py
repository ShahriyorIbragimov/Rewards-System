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

@router.get("/validate", response_model=s.StudentOut)
def validate(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.student):
        student = c.validate(db=db, data=s.StudentCreate(
            user_id=current_user.id,
            coin_balance=0,
            total_coins_earned=0,
            total_coins_spent=0,
            avatar_url=current_user.photo_url,
            bio="",
            is_active=True
        ))
        if student:
            return student

@router.get("/list-all", response_model=List[s.StudentOut])
def list_all_student_profiles(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        students = c.get_students(db)
        return students

@router.get("/list-active", response_model=List[s.StudentOut])
def list_active_student_profiles(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        students = c.get_active_students(db)
        return students

@router.get("/list-inactive", response_model=List[s.StudentOut])
def list_inactive_student_profiles(db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        students = c.get_inactive_students(db)
        return students

@router.get(f"/list/{id}", response_model=s.StudentOut)
def list_one_student_profile(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        student = c.get_student(id=id, db=db)
        return student

@router.post("/create", response_model=s.StudentOut)
def create_student(data: s.StudentCreate, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        student = c.create_student(db, data)
        return student

@router.put("/update-student-profile", response_model=s.StudentOut)
def update_student_profile(data: s.StudentUpdate, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        student = c.update_student(db, data)
        return student

@router.put(f"/deactivate/{id}", response_model=s.StudentOut)
def deactivate_user(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        student = c.deactivate_student(db=db, id=id)
        return student

@router.delete(f"/delete/{id}", response_model=s.StudentOut)
def delete_student_profile(id: uuid.UUID, db: Session = Depends(getDB), current_user: um.Users = Depends(get_current_user)):
    if isWho(current_user, um.Role.admin):
        student = c.delete_student(db=db, id=id)
        return student
