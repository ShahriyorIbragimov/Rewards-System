from pydantic import BaseModel
from typing import Optional
from users.schemas import UserOut
import uuid

class StudentCreate(BaseModel):
    user_id: Optional[uuid.UUID] = None
    coin_balance: Optional[int] = 0
    total_coins_earned: Optional[int] = 0
    total_coins_spent: Optional[int] = 0
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = True

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
