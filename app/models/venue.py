from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from sqlalchemy import String, UniqueConstraint





class Venue(Base):
    __tablename__ = "venues"

    __table_args__ = (UniqueConstraint("name", "location",name="uq_venue_name_location"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))

    seat: Mapped["Seat"] = relationship(back_populates="venue")
    event: Mapped["Event"] = relationship(back_populates="venue")