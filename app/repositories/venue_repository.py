from sqlalchemy.orm import Session
from app.models.venue import Venue



def create_venue(db: Session, name:str, location:str):
    venue = Venue(name = name, location = location)
    db.add(venue)
    db.commit()
    db.refresh(venue)

    return venue


def get_venue_by_name_and_location(db:Session, name:str,location:str):
    return db.query(Venue).filter(Venue.name == name, Venue.location == location).first()



def get_venues(db:Session):
    return db.query(Venue).all()