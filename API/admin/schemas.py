from pydantic import BaseModel
from uuid import UUID

class AdminCreate(BaseModel):
    user_id: UUID
    avatar_url: str
    bio: str
    is_active: bool

class AdminOut(AdminCreate):
    id: UUID

    class Config:
        from_attributes = True

class AdminUpdate(BaseModel):
    user_id: UUID
    avatar_url: str
    bio: str
    is_active: bool
