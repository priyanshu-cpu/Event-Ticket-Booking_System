from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Boolean, ForeignKey, String, Enum as SAEnum, Integer
from app.db.database import Base
from datetime import datetime, UTC
from app.models.enums import BookingStatus


class Booking(Base):
    __tablename__ = "bookings"

    id : Mapped[int] = mapped_column(primary_key=True)
    event_id : Mapped[int] = mapped_column(ForeignKey("events.id"))
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    seat_id : Mapped[int] = mapped_column(ForeignKey("seats.id"))
    status: Mapped[BookingStatus] = mapped_column(SAEnum(BookingStatus, name = "booking_status"), default=BookingStatus.pending, server_default="pending")
    hold_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    seat : Mapped["Seat"] = relationship(back_populates="booking")
    user : Mapped["User"] = relationship(back_populates="booking")
    event : Mapped["Event"] = relationship(back_populates="booking")