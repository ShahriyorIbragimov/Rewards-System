from pydantic import BaseModel
from typing import Optional
from users.schemas import UserOut
import uuid

class StudentCreate(BaseModel):
    user_id: Optional[int] = None
    avatar_url: str
    bio: str
    is_active: bool

class StudentOut(StudentCreate):
    id: uuid.UUID
    
    class Config:
        from_attributes = True

class StudentOutWithUser(StudentCreate):
    id: uuid.UUID
    user: UserOut
    
    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    id: uuid.UUID
    avatar_url: str
    bio: str
    is_active: bool
