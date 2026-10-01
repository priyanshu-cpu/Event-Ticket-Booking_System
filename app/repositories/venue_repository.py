from sqlalchemy.orm import Session
from app.models.venue import Venue



def create_venue(db: Session, name:str, location:str):
    venue = Venue(name = name, location = location)
    db.add(venue)
    db.commit()
    db.refresh(venue)

    return venue


def get_venue_by_name(db:Session, name:str):
    return db.query(Venue).filter(Venue.name == name).first()


def get_venue_by_id(db:Session, id: int):
    return db.query(Venue).filter(Venue.id == id).first()
