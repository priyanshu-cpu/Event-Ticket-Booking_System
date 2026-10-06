from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import event_repository
from app.models.event import Event
from app.schemas.event import EventBase, EventCreateResponse, EventOut




def create_event(data: EventBase, db:Session):
    event = event_repository.get_event_by_id(data.venue_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="no venue with id")

    return event_repository.create_event(data, db)


def get_event(event_id: int, db:Session):
    event = event_repository.get_event_by_id(event_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="not found")

    return event


def update_event(venue_id: int, event_id: int, form_data: EventBase, db:Session):
    event = event_repository.get_event_by_id(event_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="not found")

    return event_repository.update(venue_id, event_id, form_data, db)
