from sqlalchemy.orm import Session

from app.repositories import venue_repository
from app.schemas.venue import VenueCreate



def create_venue(db:Session, venue_data:VenueCreate):
    return venue_repository.create_venue(db, venue_data.name, venue_data.location)



