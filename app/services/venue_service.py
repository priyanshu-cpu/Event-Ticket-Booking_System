from sqlalchemy.orm import Session

from app.repositories import venue_repository
from app.schemas.venue import VenueCreate



def create_venue(db:Session, venue_data:VenueCreate):
    existing_venue = venue_repository.get_venue_by_name_and_location(db, venue_data.name, venue_data.location)

    if existing_venue:
        raise ValueError("Venue already exists")

    return venue_repository.create_venue(db, venue_data.name, venue_data.location)



