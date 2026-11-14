from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.seats import Seat




async def get_seats_by_venue_id(venue_id:int, db:AsyncSession):
    result = (await db.scalars(select(Seat).where(Seat.venue_id == venue_id))).all()
    return result

async def get_seat_by_id(seat_id: int, db: AsyncSession):
    return await db.scalar(select(Seat).where(Seat.id == seat_id))


async def get_seat_for_update(seat_id: int, db: AsyncSession):
    seat = await db.scalar(select(Seat).where(Seat.id == seat_id).with_for_update())
    return seat