from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Venue(Base):
    __tablename__ = "venues"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    location = Column(String, nullable=False)
    