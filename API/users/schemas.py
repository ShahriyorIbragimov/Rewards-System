from pydantic import BaseModel
from .models import Role
import uuid

class UserCreate(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
    photo_url: str
    role: Role

class UserOut(UserCreate):
    id: uuid.UUID
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    language_code: str
