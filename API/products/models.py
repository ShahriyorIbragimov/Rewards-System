from sqlalchemy import String, UUID, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import uuid
from mixins import TimestampMixin

class Products(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column()
    stock_quantity: Mapped[int] = mapped_column()
    image_url: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_featured: Mapped[bool] = mapped_column(default=False)
    sort_order: Mapped[int] = mapped_column(default=0)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("admin_profiles.id"))

    admin_profiles: Mapped["AdminProfiles"] = relationship(back_populates="products") # type: ignore
    order_items: Mapped[list["OrderItems"]] = relationship(back_populates="product") # type: ignore
