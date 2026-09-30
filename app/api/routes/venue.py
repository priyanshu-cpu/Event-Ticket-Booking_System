from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.venue import VenueCreateResponse, VenueOut, VenueCreate
from app.services import venue_service



router = APIRouter(prefix="/venue", tags=["Venues"])



@router.post("/create", response_model=VenueOut)
def create_venue(venue: VenueCreate, db:Session = Depends(get_db)):
    return venue_service.create_venue(db, venue)
