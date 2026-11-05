from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db.database import Base



class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(primary_key=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id", ondelete="cascade"), index=True)
    row: Mapped[str] 
    seat_number: Mapped[int]

    venue: Mapped["Venue"] = relationship(back_populates="seats")
