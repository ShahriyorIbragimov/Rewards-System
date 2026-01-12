from uuid import UUID
from sqlalchemy import UUID, String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import uuid
from enum import Enum
from mixins import TimestampMixin

class NotificationType(str, Enum):
    reward = "reward"
    purchase = "purchase"
    order_status = "order_status"
    system = "system"

class Notifications(TimestampMixin, Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    notification_type: Mapped[NotificationType] = mapped_column(
        SQLEnum(NotificationType, name="notification_type_enum"),
        default=NotificationType.purchase,
        nullable=False
    )
    is_read: Mapped[bool] = mapped_column(default=False)
    related_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
    )

    user: Mapped["Users"] = relationship(back_populates="notifications") # type: ignore
