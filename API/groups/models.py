from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Text, UUID, ForeignKey, Enum as SQLEnum
import uuid
from mixins import TimestampMixin
from enum import Enum
from datetime import datetime
from sqlalchemy import DateTime, func

class Member(str, Enum):
    teacher = "teacher"
    student = "student"

class Groups(TimestampMixin, Base):
    __tablename__ = "groups"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    by_teacher: Mapped[uuid.UUID] = mapped_column(ForeignKey("teacher_profiles.id"))
    by_admin: Mapped[uuid.UUID] = mapped_column(ForeignKey("admin_profiles.id"))

    teacher_profiles: Mapped["TeacherProfiles"] = relationship(back_populates="groups") # type: ignore
    admin_profiles: Mapped["AdminProfiles"] = relationship(back_populates="groups") # type: ignore
    group_memberships: Mapped[list["GroupMemberships"]] = relationship(back_populates="group")
    rewards: Mapped[list["Rewards"]] = relationship(back_populates="group") # type: ignore

class GroupMemberships(Base):
    __tablename__ = "group_memberships"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("groups.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    role: Mapped[Member] = mapped_column(
        SQLEnum(Member, name="member_enum"),
        default=Member.student,
        nullable=False
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    group: Mapped["Groups"] = relationship(back_populates="group_memberships")
    user: Mapped["Users"] = relationship(back_populates="group_memberships") # type: ignore
