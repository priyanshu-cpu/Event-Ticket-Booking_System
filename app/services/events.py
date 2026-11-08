from app.repositories import events as event_repo, venue as venue_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFound, AlreadyExists, Unauthorized, DoesntExist
from app.schemas.event import EventCreate, EventUpdate
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


async def update_event(event_id: int, event_data: EventUpdate, db:AsyncSession, user:User):
    if not user.email == settings.SECRET_EMAIL.get_secret_value():
        raise Unauthorized
    event = await event_repo.get_event_by_id(event_id, db)
    if event is None:
        raise NotFound
    if event_data.venue_id is not None:
        existing_venue = await venue_repo.get_venue_by_id(event_data.venue_id, db)
        if existing_venue is None:
            raise DoesntExist
    update_data = event_data.model_dump(exclude_unset=True)
    if not update_data:
        return event
    return await event_repo.update_event(update_data, event, db)


async def delete_event(event_id: int, db:AsyncSession, user:User):
    if user.email !=  settings.SECRET_EMAIL.get_secret_value():
        raise Unauthorized
    event = await event_repo.get_event_by_id(event_id, db)
    if event is None:
        raise NotFound
    return await event_repo.delete_event(event, db)