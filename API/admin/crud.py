from sqlalchemy.orm import Session
from . import schemas as s
from . import models as m
from fastapi import HTTPException, status
import uuid

def create_admin(db: Session, data: s.AdminCreate):
    try:
        admin = db.query(m.AdminProfiles).filter(
            m.AdminProfiles.user_id == data.user_id
        ).first()
        if admin:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Admin profile with this user already exists.",
            )
        admin_data = data.model_dump()
        admin = m.StudentProfiles(**admin_data)
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

# def update_student(db: Session, data: s.StudentUpdate):
#     try:
#         student = db.query(m.StudentProfiles).filter(m.StudentProfiles.id == data.id).first()
#         if not student:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Student profile is not found."
#             )
#         for key, value in data.model_dump().items():
#             setattr(student, key, value)
#         db.commit()
#         db.refresh(student)
#         return student
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )

# def get_students(db: Session):
#     try:
#         return db.query(m.StudentProfiles).all()
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e),
#         )
    
# def get_active_students(db: Session):
#     try:
#         return db.query(m.StudentProfiles).filter(m.StudentProfiles.is_active == True).all()
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e),
#         )
    
# def get_inactive_students(db: Session):
#     try:
#         return db.query(m.StudentProfiles).filter(m.StudentProfiles.is_active == False).all()
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e),
#         )

# def get_student(db: Session, id: uuid.UUID):
#     try:
#         student = db.query(m.StudentProfiles).filter(m.StudentProfiles.id == id).first()
#         if not student:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="User is not found."
#             )
#         return student
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e),
#         )

# def delete_student(db: Session, id: uuid.UUID):
#     try:
#         student = get_student(db=db, id=id)
#         db.delete(student)
#         db.commit()
#         return student
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e),
#         )
    
# def deactivate_student(db: Session, id: uuid.UUID):
#     try:
#         student = get_student(db=db, id=id)
#         student.is_active = False
#         db.commit()
#         db.refresh(student)
#         return student
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e),
#         )