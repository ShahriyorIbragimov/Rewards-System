from pydantic import BaseModel
from uuid import UUID

class GroupCreate(BaseModel):
    title: str
    description: str
    is_active: bool
    created_by: UUID

class GroupOut(GroupCreate):
    id: UUID

    class Config:
        from_attributes = True

class GroupUpdate(BaseModel):
    title: str
    description: str
    is_active: bool
