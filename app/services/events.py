from app.repositories import events as event_repo, venue as venue_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFound, AlreadyExists, Unauthorized
from app.schemas.event import EventCreate
from app.models.user import User
from app.core.config import settings


async def get_events(venue_id: int, db: AsyncSession):
    venue = await venue_repo.get_venue_by_id(venue_id, db)
    if venue is None:
        raise NotFound
    events = await event_repo.get_events_by_venue_id(venue_id, db)
    if events is None:
        raise NotFound
    return events


async def get_event(event_id: int, db: AsyncSession):
    event = await event_repo.get_event_by_id(event_id, db)
    if event is None:
        raise NotFound
    return event


async def create_event(event:EventCreate, db:AsyncSession, user:User):
    if user.email != settings.SECRET_EMAIL.get_secret_value():
        raise Unauthorized
    venue = await venue_repo.get_venue_by_id(event.venue_id, db)
    if not venue:
        raise NotFound

    result = await event_repo.create_event(event, db)
    return result