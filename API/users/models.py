from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, BigInteger, Enum as SQLEnum, UUID
import uuid
from enum import Enum
from mixins import TimestampMixin

class Role(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class Users(TimestampMixin, Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(150))
    language_code: Mapped[str] = mapped_column(String(3))
    photo_url: Mapped[str] = mapped_column()
    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, name="role_enum"),
        default=Role.student,
        nullable=False
    )
    
    group_memberships: Mapped[list["GroupMemberships"]] = relationship(back_populates="user") # type: ignore
    admin_profiles: Mapped[list["AdminProfiles"]] = relationship(back_populates="user") # type: ignore
    teacher_profiles: Mapped[list["TeacherProfiles"]] = relationship(back_populates="user") # type: ignore
    student_profiles: Mapped[list["StudentProfiles"]] = relationship(back_populates="user") # type: ignore
    notifications: Mapped[list["Notifications"]] = relationship(back_populates="user") # type: ignore
