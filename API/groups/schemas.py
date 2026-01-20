from pydantic import BaseModel
from uuid import UUID
from mixins import CreatedBy
from models import Member

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

class MemberCreate(BaseModel):
    group_id: UUID
    user_id: UUID
    role: Member

class MemberOut(MemberCreate):
    id: UUID

    class Config:
        from_attributes = True
