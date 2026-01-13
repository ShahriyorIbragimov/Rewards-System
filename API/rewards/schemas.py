from pydantic import BaseModel
from ..mixins import CreatedBy
import uuid

class RewardCreate(BaseModel):
    by_teacher: uuid.UUID
    by_admin: uuid.UUID
    created_by: CreatedBy
    student_id: uuid.UUID
    group_id: uuid.UUID
    amount: int
    reason: str

class RewardOut(BaseModel):
    id: uuid.UUID
    by_teacher: uuid.UUID
    by_admin: uuid.UUID
    created_by: CreatedBy
    student_id: uuid.UUID
    group_id: uuid.UUID
    amount: int
    reason: str
    created_at: str  # or datetime
    updated_at: str