from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.exceptions import ValueAlreadyExistsException

from app.db.session import get_db
from app.schemas.venue import VenueCreateResponse, VenueOut, VenueCreate
from app.services import venue_service



router = APIRouter(prefix="/venue", tags=["Venues"])



@router.post("/create", response_model=VenueCreateResponse)
def create_venue(venue: VenueCreate, db:Session = Depends(get_db)):
    try:
        new_venue = venue_service.create_venue(db, venue)
    except ValueAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Venue already exists")
    
    return {
        "message" : "venue created",
        "data" : new_venue
    }