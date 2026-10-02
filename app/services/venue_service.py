from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories import venue_repository
from app.schemas.venue import VenueCreate



def create_venue(db:Session, venue_data:VenueCreate):
    existing_venue = venue_repository.get_venue_by_name_and_location(db, venue_data.name, venue_data.location)

    if existing_venue:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Venue already exists")

    return venue_repository.create_venue(db, venue_data.name, venue_data.location)



def get_venues(db:Session):
    venues = venue_repository.get_venues(db)

    if venues is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No venues found")

    return venues