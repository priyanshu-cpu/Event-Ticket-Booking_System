from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, exists
from app.models.venue import Venue




async def get_venues(db:AsyncSession):
    result = (await db.scalars(select(Venue))).all()
    return result


async def get_venue_by_id(venue_id: int, db:AsyncSession):
    result = await  db.scalar(select(Venue).where(Venue.id == venue_id))
    return result