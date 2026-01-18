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

class UserOut(BaseModel):
    id: uuid.UUID
    telegram_id: int
    phone_number: str
    first_name: str
    last_name: str
    role: Role
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str

class UserPasswordUpdate(BaseModel):
    id: uuid.UUID
    old_password: str
    new_password: str
