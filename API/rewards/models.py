from sqlalchemy import UUID, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import uuid
from mixins import TimestampMixin, CreatedByMixin

class Rewards(TimestampMixin, CreatedByMixin, Base):
    __tablename__ = "rewards"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("student_profiles.id"))
    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("groups.id"))
    amount: Mapped[int] = mapped_column()
    reason: Mapped[str] = mapped_column(Text)

    student_profiles: Mapped["StudentProfiles"] = relationship(back_populates="rewards") # type: ignore
    group: Mapped["Groups"] = relationship(back_populates="rewards") # type: ignore
