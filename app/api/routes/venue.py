from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session


from app.db.session import get_db
from app.schemas.venue import VenueCreateResponse, VenueOut, VenueCreate
from app.services import venue_service



router = APIRouter(prefix="/venue", tags=["Venues"])



@router.post("/create", response_model=VenueCreateResponse)
def create_venue(venue: VenueCreate, db:Session = Depends(get_db)):
    new_venue = venue_service.create_venue(db, venue)

    return {
        "message" : "venue created",
        "data" : new_venue
    }



@router.get("/get", response_model=list[VenueOut])
def get_venues(db:Session = Depends(get_db)):
    return venue_service.get_venues(db)
