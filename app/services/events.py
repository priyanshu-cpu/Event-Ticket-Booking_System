from app.repositories import events as event_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFound


async def get_events(venue_id: int, db: AsyncSession):
    events = await event_repo.get_events_by_venue_id(venue_id, db)
    if events is None:
        raise NotFound
    return events


async def get_event(event_id: int, db: AsyncSession):
    event = await event_repo.get_event_by_id(event_id, db)
    if event is None:
        raise NotFound
    return event
