from sqlalchemy import UUID, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import uuid
from enum import Enum
from mixins import TimestampMixin, CreatedByMixin

class TransactionType(str, Enum):
    reward = "reward"
    purchase = "purchase"
    refund = "refund"
    admin_adjustment = "admin_adjustment"

class Transactions(TimestampMixin, CreatedByMixin, Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("student_profiles.id"))
    amount: Mapped[int] = mapped_column()
    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLEnum(TransactionType, name="transaction_type_enum"),
        default=TransactionType.purchase,
        nullable=False
    )
    balance_after: Mapped[int] = mapped_column()
    reference_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(Text)

    student_profiles: Mapped["StudentProfiles"] = relationship(back_populates="transactions") # type: ignore
