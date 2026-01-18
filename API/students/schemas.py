from pydantic import BaseModel
import uuid

class StudentCreate(BaseModel):
    user_id: int
    avatar_url: str
    bio: str
    is_active: bool

class StudentOut(StudentCreate):
    id: uuid.UUID
    
    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    id: uuid.UUID
    avatar_url: str
    bio: str
    is_active: bool
