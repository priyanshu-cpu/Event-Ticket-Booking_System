from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventBase




def create_event(data: EventBase, db:Session):
    new_event = Event(
        venue_id = data.venue_id,
        name = data.name,
        description = data.description,
        event_date = data.event_date,
        start_time = data.start_time,
        end_time  = data.end_time,
        ticket_price = data.ticket_price
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event