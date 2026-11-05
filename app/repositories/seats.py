from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.seats import Seat




async def get_seats(db:AsyncSession):
    result = (await db.scalars(select(Seat))).all()
    return result