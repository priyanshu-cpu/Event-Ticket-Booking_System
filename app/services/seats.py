from app.repositories import seats as seat_repo, venue as venue_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFound



async def get_seats(venue_id:int, db:AsyncSession):
    venue = await venue_repo.get_venue_by_id(venue_id, db)
    if venue is None:
        raise NotFound
    seats = await seat_repo.get_seats_by_venue_id(venue_id,db)
    return seats
