from sqlalchemy.orm import Session
from app.models.venue import Venue



def create_venue(db: Session, name:str, location:str):
    venue = Venue(name = name, location = location)
    db.add(venue)
    db.commit()
    db.refresh(venue)

    return venue