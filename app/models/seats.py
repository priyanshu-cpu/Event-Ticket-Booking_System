from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


class Seat(Base):
    __tablename__ = "seats"

    __table_args__ = (UniqueConstraint("venue_id", "row", "seat_number", name="uq_seat_venue_position"),)


    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    row = Column(String, nullable=False)
    seat_number = Column(Integer, nullable=False)

    venue = relationship("Venue",  back_populates="seat")
    bookings = relationship("Booking", back_populates="seat")