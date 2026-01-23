from sqlalchemy.orm import Session
from . import schemas as s
from . import models as m
from fastapi import HTTPException, status
import uuid

def create_notification(db: Session, data: s.NotificationCreate):
    try:
        notification_data = data.model_dump()
        notification = m.Notifications(**notification_data)
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def update_notification(db: Session, data: s.NotificationUpdate):
    try:
        notification = db.query(m.Notifications).filter(m.Notifications.id == data.id).first()
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notification is not found."
            )
        for key, value in data.model_dump().items():
            setattr(notification, key, value)
        db.commit()
        db.refresh(notification)
        return notification
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

def get_notifications(db: Session):
    try:
        return db.query(m.Notifications).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_read_notifications(db: Session):
    try:
        return db.query(m.Notifications).filter(m.Notifications.is_read == True).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
def get_unread_notifications(db: Session):
    try:
        return db.query(m.Notifications).filter(m.Notifications.is_read == False).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def get_notification(db: Session, id: uuid.UUID):
    try:
        notification = db.query(m.Notifications).filter(m.Notifications.id == id).first()
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Group is not found."
            )
        return notification
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

def delete_notification(db: Session, id: uuid.UUID):
    try:
        notification = get_notification(db=db, id=id)
        db.delete(notification)
        db.commit()
        return notification
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
