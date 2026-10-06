from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.event import EventBase, EventOut, EventCreateResponse
from app.services import event_service



router = APIRouter(prefix="/venues", tags=["Events"])



@router.post("/{venue_id}/events", response_model=EventCreateResponse, status_code=201)
def create_event(venue_id:int, data:EventBase, db:Session = Depends(get_db)):
    event = event_service.create_event(venue_id,data, db)
    return{
        "message" : "event created",
        "data" : event
    }



@router.get("/{venue_id}/events", response_model=list[EventOut])
def get_events(venue_id: int,db:Session = Depends(get_db)):
    return event_service.get_events(venue_id, db)


@router.get("/events/{event_id}", response_model=EventOut)
def get_event(event_id: int,db:Session = Depends(get_db)):
    return event_service.get_event(event_id, db)




@router.put("/{venue_id}/events/{event_id}", response_model= EventCreateResponse)
def update_event(venue_id: int, event_id: int ,form_data: EventBase, db: Session = Depends(get_db)):
    updated_event = event_service.update_event(venue_id, event_id, form_data, db)
    return{
        "message" : "updated",
        "data" : updated_event
    }


@router.delete("/events/{event_id}")
def delete_event(event_id: int, db:Session = Depends(get_db)):
    return event_service.delete_event(event_id, db)