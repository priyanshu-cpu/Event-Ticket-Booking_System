from app.repositories import venue as venue_repo
from sqlalchemy.ext.asyncio import AsyncSession




async def get_venues(db:AsyncSession):
    return await venue_repo.get_venues(db)