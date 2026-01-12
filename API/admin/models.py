from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, UUID, ForeignKey, Text
import uuid
from mixins import TimestampMixin

class AdminProfiles(TimestampMixin, Base):
    __tablename__ = "admin_profiles"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["Users"] = relationship(back_populates="admin_profiles") # type: ignore
    groups: Mapped[list["Groups"]] = relationship(back_populates="admin_profiles") # type: ignore
    issued_rewards: Mapped[list["Rewards"]] = relationship(back_populates="admin_profiles") # type: ignore
    products: Mapped[list["Products"]] = relationship(back_populates="admin_profiles") # type: ignore
    transactions: Mapped[list["Transactions"]] = relationship(back_populates="admin_profiles") # type: ignore
    