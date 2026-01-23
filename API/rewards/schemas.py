from pydantic import BaseModel
from mixins import CreatedBy
import uuid

class RewardCreate(BaseModel):
    created_by: CreatedBy
    student_id: uuid.UUID
    group_id: uuid.UUID
    amount: int
    reason: str

class RewardOut(RewardCreate):
    id: uuid.UUID
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True