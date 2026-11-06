from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from app.db.database import Base



class Seat(Base):
    __tablename__ = "seats"

    __table_args__ = (UniqueConstraint("venue_id", "row", "seat_number", name="uq_seat_venue_position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id", ondelete="cascade"), index=True)
    row: Mapped[str] 
    seat_number: Mapped[int]

    venue: Mapped["Venue"] = relationship(back_populates="seat")
    booking : Mapped["booking"] = relationship(back_populates="seat")