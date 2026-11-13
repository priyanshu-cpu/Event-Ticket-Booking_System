from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, exists
from app.models.booking import Booking
from app.schemas.bookings import BookingResponse, BookingCreate, BookingStatus
from app.models.user import User



async def get_bookings(db: AsyncSession, user: User):
    result = (await db.scalars(select(Booking).where(Booking.user_id == user.id))).all()
    return result


async def get_booking_by_id(booking_id: int, db: AsyncSession, user: User):
    result = await db.scalar(select(Booking).where(Booking.id == booking_id, Booking.user_id == user.id))
    return result