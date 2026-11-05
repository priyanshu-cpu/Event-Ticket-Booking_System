from app.repositories import venue as venue_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFound




async def get_venues(db:AsyncSession):
    return await venue_repo.get_venues(db)


async def get_venue(venue_id: int, db:AsyncSession):
    venue = await venue_repo.get_venue_by_id(venue_id, db)
    if venue is None:
        raise NotFound

    return venue