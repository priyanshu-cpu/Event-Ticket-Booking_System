from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime, UTC


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")
    hold_expires_at = Column(DateTime, nullable=True, default=None)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    seat = relationship("Seat", back_populates="bookings")
    user = relationship("Users", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")
