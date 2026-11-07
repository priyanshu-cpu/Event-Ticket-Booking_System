from app.repositories import venue as venue_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFound
from app.schemas.venue import VenueCreate
from app.models.user import User
from app.core.exceptions import AlreadyExists, Unauthorized
from app.core.config import settings




async def get_venues(db:AsyncSession):
    return await venue_repo.get_venues(db)


async def get_venue(venue_id: int, db:AsyncSession):
    venue = await venue_repo.get_venue_by_id(venue_id, db)
    if venue is None:
        raise NotFound

    return venue


async def create_venue(venue_data:VenueCreate, user: User, db:AsyncSession):
    if user.email != settings.SECRET_EMAIL.get_secret_value():
        raise Unauthorized
    existing_venue = await venue_repo.get_venue_by_name_location(venue_data.name, venue_data.location, db)

    if existing_venue:
        raise AlreadyExists

    venue = await venue_repo.create_venue(venue_data.name, venue_data.location, db)
    return venue


async def delete_venue(venue_id: int, db:AsyncSession, user:User):
    if user.email != settings.SECRET_EMAIL.get_secret_value():
        raise Unauthorized
    venue = await venue_repo.get_venue_by_id(venue_id, db)
    if venue is None:
        raise NotFound
    return await venue_repo.delete_venue(venue, db)