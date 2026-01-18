from datetime import datetime
from sqlalchemy import DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import TypeDecorator
from pydantic import BaseModel, ValidationError
import uuid
from enum import Enum


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Role(str, Enum):
    admin = "admin"
    teacher = "teacher"


class CreatedBy(BaseModel):
    role: Role
    user_id: uuid.UUID


class CreatedByType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, dict):
                try:
                    CreatedBy(**value)
                except ValidationError as e:
                    raise ValueError(f"Invalid created_by structure: {e}")
                # Convert UUID to string in dict
                if 'user_id' in value and isinstance(value['user_id'], uuid.UUID):
                    value['user_id'] = str(value['user_id'])
            elif isinstance(value, CreatedBy):
                value_dict = value.model_dump()
                value_dict['user_id'] = str(value.user_id)
                value = value_dict
            else:
                raise ValueError("created_by must be a dict or CreatedBy instance")
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return CreatedBy(**value)
        return value


class CreatedByMixin:
    created_by: Mapped[CreatedBy] = mapped_column(CreatedByType)
