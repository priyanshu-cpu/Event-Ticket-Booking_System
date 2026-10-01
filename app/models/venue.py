from sqlalchemy import Column, Integer, String, UniqueConstraint

from app.db.database import Base


class Venue(Base):
    __tablename__ = "venues"
    __table_args__ = (UniqueConstraint("name", "location", name="uq_venue_name_location"),)


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    location = Column(String, nullable=False)
    