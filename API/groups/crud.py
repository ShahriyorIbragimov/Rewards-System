from sqlalchemy.orm import Session
from . import schemas as s
from . import models as m
from fastapi import HTTPException, status
import uuid

def create_group(db: Session, data: s.GroupCreate):
    try:
        group = db.query(m.Groups).filter(
            m.Groups.title == data.title
        ).first()
        if group:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Group with this title already exists.",
            )
        group_data = data.model_dump()
        group = m.Groups(**group_data)
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
    
def get_active_groups(db: Session):
    try:
        return db.query(m.Groups).filter(m.Groups.is_active == True).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
def get_inactive_groups(db: Session):
    try:
        return db.query(m.Groups).filter(m.Groups.is_active == False).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
def get_user_groups(user_id: uuid.UUID, db: Session):
    try:
        return db.query(m.Groups).filter(
            m.Groups.is_active.is_(True),
            m.Groups.group_memberships.any(m.GroupMemberships.user_id == user_id),
        ).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_group(db: Session, id: uuid.UUID):
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

def delete_group(db: Session, id: uuid.UUID):
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
    
def deactivate_group(db: Session, id: uuid.UUID):
    try:
        group = get_group(db=db, id=id)
        group.is_active = False
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
    
def add_member(db: Session, data: s.MemberCreate):
    try:
        member = db.query(m.GroupMemberships).filter(
            m.GroupMemberships.user_id == data.user_id
        ).first()
        if member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This user is already in this group.",
            )
        member_data = data.model_dump()
        member = m.Groups(**member_data)
        db.add(member)
        db.commit()
        db.refresh(member)
        return member
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
def get_members(group_id: uuid.UUID, db: Session):
    try:
        return db.query(m.GroupMemberships).filter(m.GroupMemberships.group_id == group_id).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_member(id: uuid.UUID, db: Session):
    try:
        return db.query(m.GroupMemberships).filter(m.GroupMemberships.id == id).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
def delete_member(db: Session, id: uuid.UUID):
    try:
        member = get_member(db=db, id=id)
        db.delete(member)
        db.commit()
        return member
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )