from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, exists
from app.models.venue import Venue




async def get_venues(db:AsyncSession):
    result = (await db.scalars(select(Venue))).all()
    return result


async def get_venue_by_id(venue_id: int, db:AsyncSession):
    result = await  db.scalar(select(Venue).where(Venue.id == venue_id))
    return result


async def get_venue_by_name_location(name:str, locaiton:str, db:AsyncSession):
    venue = await db.scalar(select(Venue).where(Venue.name == name, Venue.location == locaiton))
    return venue


async def create_venue(name: str, location: str, db: AsyncSession):
    venue = Venue(name = name, location= location)
    db.add(venue) 
    await db.commit()
    await db.refresh(venue)

    return venue


async def delete_venue(venue: Venue, db: AsyncSession):
    await db.delete(venue)
    await db.commit()

    return {}