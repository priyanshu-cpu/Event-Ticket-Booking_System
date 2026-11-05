from app.repositories import seats as seat_repo
from sqlalchemy.ext.asyncio import AsyncSession



async def get_seats(db:AsyncSession):
    return await seat_repo.get_seats(db)