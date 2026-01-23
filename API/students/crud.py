from sqlalchemy.orm import Session
from . import schemas as s
from . import models as m
from fastapi import HTTPException, status
import uuid

def validate(db: Session, data: s.StudentCreate):
    try:
        student = db.query(m.StudentProfiles).filter(
            m.StudentProfiles.user_id == data.user_id
        ).first()
        if student:
            return student
        student_data = data.model_dump()
        student = m.StudentProfiles(**student_data)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def create_student(db: Session, data: s.StudentCreate):
    try:
        student = db.query(m.StudentProfiles).filter(
            m.StudentProfiles.user_id == data.user_id
        ).first()
        if student:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Student profile with this user already exists.",
            )
        student_data = data.model_dump()
        student = m.StudentProfiles(**student_data)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def update_student(db: Session, data: s.StudentUpdate):
    try:
        student = db.query(m.StudentProfiles).filter(m.StudentProfiles.id == data.id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student profile is not found."
            )
        for key, value in data.model_dump().items():
            setattr(student, key, value)
        db.commit()
        db.refresh(student)
        return student
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

def get_students(db: Session):
    try:
        return db.query(m.StudentProfiles).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
def get_active_students(db: Session):
    try:
        return db.query(m.StudentProfiles).filter(m.StudentProfiles.is_active == True).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
def get_inactive_students(db: Session):
    try:
        return db.query(m.StudentProfiles).filter(m.StudentProfiles.is_active == False).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_student(db: Session, id: uuid.UUID):
    try:
        student = db.query(m.StudentProfiles).filter(m.StudentProfiles.id == id).first()
        if not student:
            return
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def delete_student(db: Session, id: uuid.UUID):
    try:
        student = get_student(db=db, id=id)
        db.delete(student)
        db.commit()
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
def deactivate_student(db: Session, id: uuid.UUID):
    try:
        student = get_student(db=db, id=id)
        student.is_active = False
        db.commit()
        db.refresh(student)
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )