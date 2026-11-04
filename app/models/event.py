from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Boolean, ForeignKey, String, Enum as SAEnum, Integer
from app.db.database import Base
from datetime import datetime
from app.models.enums import EventStatus




class Event(Base):
    __tablename__ = "events"

    id:Mapped[int] = mapped_column(primary_key=True)
    venue_id : Mapped[int] = mapped_column(ForeignKey("venues.id", ondelete="restrict"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500))
    starts_at : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status : Mapped[EventStatus] = mapped_column(SAEnum(EventStatus, name = "event_status"),default=EventStatus.draft, server_default="draft")
    ticket_price: Mapped[int] = mapped_column(Integer, default=99)


    venue: Mapped["Venue"]= relationship(back_populates="events")


