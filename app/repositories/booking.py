from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.booking import Booking
from app.schemas.bookings import BookingResponse, BookingCreate, BookingStatus
from app.models.user import User


async def get_bookings(db: AsyncSession, user: User):
    result = (await db.scalars(select(Booking).where(Booking.user_id == user.id))).all()
    return result


async def get_booking_by_id(booking_id: int, db: AsyncSession, user: User):
    result = await db.scalar(
        select(Booking).where(Booking.id == booking_id, Booking.user_id == user.id)
    )
    return result


async def get_booking_by_event_and_seat(event_id: int, seat_id: int, db: AsyncSession):
    booking = await db.scalar(
        select(Booking).where(
            Booking.event_id == event_id,
            Booking.seat_id == seat_id,
            Booking.status.in_(["held", "confirmed"]),
        )
    )
    return booking


async def create_booking(
    booking: BookingCreate,
    user: User,
    status: BookingStatus,
    expires,
    db: AsyncSession,
    commit: bool = True,
):
    new_booking = Booking(
        event_id=booking.event_id,
        seat_id=booking.seat_id,
        user_id=user.id,
        status=status,
        hold_expires_at=expires,
    )

    db.add(new_booking)
    await db.flush()
    if commit:
        await db.commit()
        await db.refresh()
    return new_booking


async def check_expired_booking(event_id: int, seat_id: int, db: AsyncSession, status: BookingStatus, current_time):
    result = await db.scalar(update(Booking).where(Booking.event_id == event_id, Booking.seat_id == seat_id, Booking.status == status,Booking.hold_expires_at < current_time).values(status= "expired"))

    return result