from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import event_repository, venue_repository
from app.schemas.event import EventBase




def create_event(data: EventBase, db:Session):
    venue = venue_repository.get_venue_by_id(data.venue_id, db)
    if not venue:
        raise HTTPException(status_code=404, detail="no venue with id")

    return event_repository.create_event(data, db)


def get_events(venue_id: int, db:Session):
    event = event_repository.get_events_by_venueId(venue_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="not found")

    return event



def get_event(event_id, db):
    event =  event_repository.get_event_by_id(event_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")

    return event



def update_event(venue_id: int, event_id: int, form_data: EventBase, db:Session):
    event = event_repository.get_event_by_id(event_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="not found")

    return event_repository.update_event(venue_id, event_id, form_data, db)


def delete_event(event_id: int, db:Session):
    event = event_repository.get_event_by_id(event_id, db)

    if not event:
        raise HTTPException(status_code=404, detail="not found")

    return event_repository.delete_event(event_id, db)