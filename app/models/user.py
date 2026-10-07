from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    email = Column(String,unique=True, nullable=True)
    pasword_hash = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    bookings = relationship("Booking", back_populates="user")