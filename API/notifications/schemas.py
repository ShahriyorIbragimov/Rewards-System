from pydantic import BaseModel
from .models import NotificationType
from uuid import UUID
from typing import Optional

class NotificationCreate(BaseModel):
    user_id: UUID
    title: str
    message: str
    notification_type: NotificationType
    is_read: bool
    related_id: Optional[UUID] = None

class NotificationOut(NotificationCreate):
    id: UUID

    class Config:
        from_attributes = True

class NotificationUpdate(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    message: str
    notification_type: NotificationType
    is_read: bool
    related_id: Optional[UUID] = None