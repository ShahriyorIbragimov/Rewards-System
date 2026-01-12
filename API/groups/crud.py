from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from . import schemas as s
from . import models as m

def create_group(db: Session, data: s.GroupCreate):
    try:
        group = db.query(m.Users).filter(
            m.Groups.title == data.title
        ).first()
        if group:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Group with this title already exists.",
            )
        group_data = data.model_dump()
        group = m.Group(**group_data)
        db.add(group)
        db.commit()
        db.refresh(group)
        return group
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def update_group(db: Session, data: s.GroupUpdate):
    try:
        group = db.query(m.Groups).filter(m.Groups.id == data.id).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Group is not found."
            )
        for key, value in data.model_dump().items():
            setattr(group, key, value)
        db.commit()
        db.refresh(group)
        return group
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

def get_groups(db: Session):
    try:
        return db.query(m.Groups).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_group(db: Session, id: UUID):
    try:
        group = db.query(m.Groups).filter(m.Groups.id == id).first()
        if not group:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Group is not found."
            )
        return group
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def delete_group(db: Session, id: UUID):
    try:
        group = get_group(db=db, id=id)
        db.delete(group)
        db.commit()
        return group
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
