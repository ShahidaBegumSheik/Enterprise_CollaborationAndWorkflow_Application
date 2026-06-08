from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    plan: Mapped[str] = mapped_column(
        String(20), default="free", nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), default="active", nullable=False, index=True
    )

    credits: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_users: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    max_storage_mb: Mapped[int] = mapped_column(Integer, default=100, nullable=False)

    provider: Mapped[str] = mapped_column(String(30), nullable=False, default="razorpay")
    razorpay_order_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )
    razorpay_payment_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )
    razorpay_subscription_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    organization = relationship("Organization", back_populates="subscription")

    __table_args__ = (Index("ix_subscription_org_status", "organization_id", "status"),)
