from sqlalchemy import UUID, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import uuid
from mixins import TimestampMixin

class Rewards(TimestampMixin, Base):
    __tablename__ = "rewards"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    teacher_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("groups.id"))
    amount: Mapped[int] = mapped_column()
    reason: Mapped[str] = mapped_column(Text)

    teacher: Mapped["Users"] = relationship( # type: ignore
        "Users",
        foreign_keys=[teacher_id],
        back_populates="teacher_rewards"
    )
    student: Mapped["Users"] = relationship( # type: ignore
        "Users",
        foreign_keys=[student_id],
        back_populates="student_rewards"
    )
    group: Mapped["Groups"] = relationship(back_populates="rewards") # type: ignore
