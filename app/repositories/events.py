from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, exists
from app.models.event import Event




async def get_events_by_venue_id(venue_id: int, db:AsyncSession):
    result = (await db.scalars(select(Event).where(Event.venue_id == venue_id))).all()
    return result



async def get_event_by_id(event_id: int, db:AsyncSession):
    result = await db.scalar(select(Event).where(Event.id == event_id))
    return result

