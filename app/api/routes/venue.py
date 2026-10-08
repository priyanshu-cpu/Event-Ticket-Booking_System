from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session


from app.db.session import get_db
from app.schemas.venue import VenueCreateResponse, VenueOut, VenueCreate
from app.services import venue_service



router = APIRouter(prefix="/venues", tags=["Venues"])



@router.post("", response_model=VenueCreateResponse, status_code=status.HTTP_201_CREATED)
def create_venue(venue: VenueCreate, db:Session = Depends(get_db)):
    new_venue = venue_service.create_venue(db, venue)

    return {
        "message" : "venue created",
        "data" : new_venue
    }



@router.get("", response_model=list[VenueOut])
def get_venues(db:Session = Depends(get_db)):
    return venue_service.get_venues(db)


@router.get("/{venue_id}", response_model=VenueOut)
def get_venue(venue_id: int, db:Session = Depends(get_db)):
    return venue_service.get_venue(venue_id, db)
