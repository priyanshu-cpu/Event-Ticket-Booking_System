from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, exists
from app.models.event import Event
from app.schemas.event import EventCreate




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