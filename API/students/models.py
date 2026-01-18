from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, UUID, ForeignKey, Integer, Text
import uuid
from mixins import TimestampMixin

class StudentProfiles(TimestampMixin, Base):
    __tablename__ = "student_profiles"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    coin_balance: Mapped[int] = mapped_column(Integer, default=0)
    total_coins_earned: Mapped[int] = mapped_column(Integer, default=0)
    total_coins_spent: Mapped[int] = mapped_column(Integer, default=0)
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["Users"] = relationship(back_populates="student_profiles") # type: ignore
    rewards: Mapped[list["Rewards"]] = relationship(back_populates="student_profiles") # type: ignore
    orders: Mapped[list["Orders"]] = relationship(back_populates="student_profiles") # type: ignore
    transactions: Mapped[list["Transactions"]] = relationship(back_populates="student_profiles") # type: ignore
    