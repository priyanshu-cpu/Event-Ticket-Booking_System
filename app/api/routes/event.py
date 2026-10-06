from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.event import EventBase, EventOut, EventCreateResponse
from app.models.event import Event
from app.services import event_service



router = APIRouter(prefix="/venue", tags=["Events"])



@router.post("/event", response_model=EventCreateResponse, status_code=201)
def create_event( data:EventBase, db:Session = Depends(get_db)):
    event = event_service.create_event(data, db)
    return{
        "message" : "event created",
        "data" : event
    }



@router.get("/{venue_id}/event", response_model=list[EventOut])
def get_event(venue_id: int,db:Session = Depends(get_db)):
    return event_service.get_event(venue_id, db)



@router.put("/{venue_id}/event", response_model= EventCreateResponse)
def update_event(venue_id: int, event_id: int ,form_data: EventBase, db: Session = Depends(get_db)):
    return event_service.update_event(venue_id, event_id, form_data, db)