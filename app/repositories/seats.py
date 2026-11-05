from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.seats import Seat




async def get_seats_by_venue_id(venue_id:int, db:AsyncSession):
    result = (await db.scalars(select(Seat).where(Seat.venue_id == venue_id))).all()
    return result