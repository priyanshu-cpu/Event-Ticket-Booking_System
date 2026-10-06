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


def get_event_by_id(id:int, db:Session):
    return db.get(Event, id)


def get_events_by_venueId(venue_id, db:Session):
    return db.query(Event).filter(Event.venue_id == venue_id).all()


def update_event(event_id: int, form_data: EventBase, db:Session):
    event = db.get(Event, event_id)


    event.venue_id = form_data.venue_id
    event.name = form_data.name
    event.description = form_data.description
    event.event_date = form_data.event_date
    event.start_time = form_data.start_time
    event.end_time = form_data.end_time
    event.ticket_price = form_data.ticket_price

    db.commit()
    db.refresh(event)

    return event



def delete_event(event_id: int, db: Session):
    event = db.get(Event, event_id)

    db.delete(event)
    db.commit()
    return {}