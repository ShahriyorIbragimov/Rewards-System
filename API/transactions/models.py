from sqlalchemy import UUID, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import uuid
from enum import Enum
from mixins import TimestampMixin

class TransactionType(str, Enum):
    reward = "reward"
    purchase = "purchase"
    refund = "refund"
    admin_adjustment = "admin_adjustment"

class Transactions(TimestampMixin, Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int] = mapped_column()
    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLEnum(TransactionType, name="transaction_type_enum"),
        default=TransactionType.purchase,
        nullable=False
    )
    balance_after: Mapped[int] = mapped_column()
    reference_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(Text)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    student: Mapped["Users"] = relationship(
        "Users",
        foreign_keys=[student_id],
        back_populates="student_transactions",
    )  # type: ignore

    creator: Mapped["Users"] = relationship(
        "Users",
        foreign_keys=[created_by],
        back_populates="created_transactions",
    )  # type: ignore
