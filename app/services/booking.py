from app.repositories import booking as booking_repo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFound, AlreadyExists, Unauthorized, DoesntExist
from app.schemas.bookings import BookingCreate, BookingStatus, BookingResponse
from app.models.user import User
from app.core.config import settings



async def get_bookings(db: AsyncSession, user: User):
    return await booking_repo.get_bookings(db, user)


async def get_booking_by_id(booking_id: int, db: AsyncSession, user: User):
    booking = await booking_repo.get_booking_by_id(booking_id, db, user)
    if booking is None:
        raise NotFound
    
    return booking