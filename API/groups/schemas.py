from pydantic import BaseModel
from uuid import UUID
from mixins import CreatedBy

class GroupCreate(BaseModel):
    title: str
    description: str
    is_active: bool
    created_by: CreatedBy

class GroupOut(GroupCreate):
    id: UUID

    class Config:
        from_attributes = True

class GroupUpdate(BaseModel):
    title: str
    description: str
    is_active: bool
