from uuid import UUID
from sqlalchemy import UUID, String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import uuid
from enum import Enum
from mixins import TimestampMixin
from datetime import datetime
from sqlalchemy import DateTime

class Status(str, Enum):
    pending = "pending"
    delivered = "delivered"
    confirmed = "confirmed"
    cancelled = "cancelled"

class Orders(TimestampMixin, Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("student_profiles.id"))
    total_coins: Mapped[int] = mapped_column()
    status: Mapped[Status] = mapped_column(
        SQLEnum(Status, name="status_enum"),
        default=Status.pending,
        nullable=False
    )
    notes: Mapped[str] = mapped_column(Text)
    delivered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    order_items: Mapped[list["OrderItems"]] = relationship(back_populates="order") # type: ignore
    student_profiles: Mapped["StudentProfiles"] = relationship(back_populates="orders") # type: ignore

class OrderItems(TimestampMixin, Base):
    __tablename__ = "order_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"))
    product_name: Mapped[str] = mapped_column(String(200))
    product_price: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    subtotal: Mapped[int] = mapped_column()

    order: Mapped["Orders"] = relationship(back_populates="order_items")
    product: Mapped["Products"] = relationship(back_populates="order_items") # type: ignore
