from pydantic import BaseModel
from .models import Role
import uuid

class UserCreate(BaseModel):
    telegram_id: int
    phone_number: str
    password_hash: str
    first_name: str
    last_name: str
    role: Role
    is_active: bool

class UserOut(BaseModel):
    id: uuid.UUID
    telegram_id: int
    phone_number: str
    first_name: str
    last_name: str
    role: Role
    is_active: bool
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    role: Role
    is_active: bool

class UserPasswordUpdate(BaseModel):
    id: uuid.UUID
    old_password: str
    new_password: str