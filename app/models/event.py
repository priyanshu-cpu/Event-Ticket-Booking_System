from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from datetime import datetime, UTC, time
from sqlalchemy.orm import relationship
from app.db.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    event_date = Column(Date, nullable=False)
    start_time = Column(time, nullable=False)
    end_time  = Column(time, nullable=False)
    ticket_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
