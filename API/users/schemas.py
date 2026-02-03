from datetime import datetime
from pydantic import BaseModel
from .models import Role
import uuid
from typing import Optional

class UserCreate(BaseModel):
    telegram_id: Optional[int] = None
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    allows_write_to_pm: Optional[bool] = None
    photo_url: Optional[str] = None
    role: Role

class UserOut(UserCreate):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    language_code: str
