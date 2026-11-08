from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, exists
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate




async def get_events_by_venue_id(venue_id: int, db:AsyncSession):
    result = (await db.scalars(select(Event).where(Event.venue_id == venue_id))).all()
    return result



async def get_event_by_id(event_id: int, db:AsyncSession):
    result = await db.scalar(select(Event).where(Event.id == event_id))
    return result



async def create_event(event:EventCreate, db:AsyncSession):
    new_event = Event(
        venue_id = event.venue_id,
        name = event.name,
        description = event.description,
        starts_at = event.starts_at,
        ticket_price = event.ticket_price
    )

    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    
    return new_event


async def update_event(update_data:dict, event:Event, db:AsyncSession):
    for field, value in update_data.items():
        setattr(event, field, value)

    await db.commit()
    await db.refresh(event)
    return event


async def delete_event(event: Event, db:AsyncSession):
    await db.delete(event)
    await db.commit()
    return 