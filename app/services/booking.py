from app.repositories import booking as booking_repo
from app.repositories import events as event_repo
from app.repositories import seats as seat_repo
from app.services import hold_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import (
    NotFound,
    EventNotFound,
    SeatNotFound,
    SeatDoesNotBelong,
    SeatHeldOrBooked,
    SeatHeld,
    Unauthorized,
    CanNotConfirm,
    BookingHoldHasExpired,
    PaymentFailed,
    SomethingWentWrong
)
from app.schemas.bookings import BookingCreate, BookingStatus, BookingResponse
from app.models.user import User
from app.core.config import settings
from datetime import datetime, timedelta, UTC


async def get_bookings(db: AsyncSession, user: User):
    return await booking_repo.get_bookings(db, user)


async def get_booking_by_id(booking_id: int, db: AsyncSession, user: User):
    booking = await booking_repo.get_booking_by_id(booking_id, db, user)
    if booking is None:
        raise NotFound

    return booking


async def create_booking(booking: BookingCreate, user: User, db: AsyncSession):
    event = await event_repo.get_event_by_id(booking.event_id, db)
    if not event:
        raise EventNotFound

    seat = await seat_repo.get_seat_for_update(booking.seat_id, db)
    if not seat:
        raise SeatNotFound

    if not seat.venue_id == event.venue_id:
        raise SeatDoesNotBelong

    check_expired_booking(booking.event_id, booking.seat_id, db)

    check_booking = await booking_repo.get_booking_by_event_and_seat(booking.event_id, booking.seat_id, db)
    if check_booking:
        await db.rollback()
        raise SeatHeldOrBooked

    acquired =await hold_service.hold_seat(booking.event_id, booking.seat_id, user.id)
    if not acquired:
        await db.rollback()
        raise SeatHeld

    try:
        expires = datetime.now(UTC) + timedelta(minutes=10)
        new_booking = await booking_repo.create_booking(booking, user, BookingStatus.held, expires, db, commit=False)
        await db.commit()
        await db.refresh(new_booking)
        return new_booking
    except Exception:
        await db.rollback()
        await hold_service.release_seat(booking.event_id, booking.seat_id, user.id)
        raise


async def confirm_booking(booking_id: int, user: User, db: AsyncSession):
    booking = await booking_repo.get_booking_by_id(booking_id, db, user)

    if not booking:
        raise NotFound

    if booking.user_id != user.id:
        raise Unauthorized

    if booking.status != "held":
        raise CanNotConfirm

    current_time = datetime.now(UTC)

    if(booking.hold_expires_at is None or booking.hold_expires_at< current_time):
        await booking_repo.update_booking_status(booking, BookingStatus.expired, db)
        db.commit()

        await hold_service.release_seat(booking.event_id, booking.seat_id, user.id)
        raise BookingHoldHasExpired

    try:
        payment_success = True
        if not payment_success:
            raise PaymentFailed

        await booking_repo.update_booking_status(booking, BookingStatus.confirmed, db)

        db.commit()
        await db.refresh(booking)

    except Exception:
        await db.rollback()
        raise 

    await hold_service.release_seat(booking.event_id, booking.seat_id, user.id)

    return booking


async def check_expired_booking(event_id: int, seat_id: int, db: AsyncSession):
    current_time = datetime.now(UTC)
    return await booking_repo.check_expired_booking(event_id, seat_id, db, current_time, status="held")