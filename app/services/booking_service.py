from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import booking_repository
from app.repositories import event_repository
from app.repositories import seat_repository
from app.schemas.booking import BookingBase
from app.models.user import Users
from app.models.bookings import Booking
from datetime import datetime, UTC, timedelta

from app.services.hold_service import hold_seat, release_seat


def create_booking(
        form_data: BookingBase,
        user:Users,
        db:Session
):

    event = event_repository.get_event_by_id(form_data.event_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")

    seat = seat_repository.get_seat_for_update(form_data.seat_id, db)
    if not seat:
        raise HTTPException(status_code=404, detail="seat not found")

    if not seat.venue_id == event.venue_id:
        raise HTTPException(status_code=400, detail="Seat does not belogs to the event!")

    check_expired_booking(form_data.event_id, form_data.seat_id, db)

    booking = booking_repository.get_booking_by_event_and_seat(form_data.event_id, form_data.seat_id, db)
    if booking:
        db.rollback()
        raise HTTPException(status_code=409, detail="seat is held or booked")


    acquired = hold_seat(form_data.event_id, form_data.seat_id, user.id)

    if not acquired:
        db.rollback()
        raise HTTPException(status_code=409, detail="seat is temporarily held by another user")


    try:
        expires = datetime.now(UTC) + timedelta(minutes=10)
        new_booking = booking_repository.create_booking(form_data, user, db, expires, status="held", commit=False)
        db.commit()
        db.refresh(new_booking)
        return new_booking

    except Exception:
        db.rollback()
        release_seat(
            form_data.event_id,
            form_data.seat_id,
            user.id
        )



def confirm_booking(
        booking_id: int,
        user:Users,
        db:Session
):
    booking = booking_repository.get_booking_by_id(booking_id,user, db)

    if not booking:
        raise HTTPException(status_code=404, detail="booking not found")

    if booking.user_id !=  user.id:
        raise HTTPException(status_code=403, detail="You can not confirm another user's booking")

    if booking.status != "held":
        raise HTTPException(status_code=400, detail=f"Can not confirm booking with staus '{booking.status}'")

    current_time = datetime.now(UTC)

    if (
        booking.hold_expires_at is None
        or booking.hold_expires_at <= current_time
    ):
        booking_repository.update_booking_status(booking, "expired", db)
        db.commit()

        release_seat(booking.event_id, booking.seat_id, user.id)
        raise HTTPException(status_code=400,detail="Booking hold hase expired")

    try:
        paymeny_success =True

        if not paymeny_success:
            raise HTTPException(status_code=400, detail="payment failed")

        booking_repository.update_booking_status(booking, "confirmed", db)

        db.commit()
        db.refresh(booking)

    except Exception:
        db.rollback()
        raise


    release_seat(booking.event_id, booking.seat_id, user.id)

    return booking




def get_bookings(user:Users, db:Session):
    return booking_repository.get_bookings(user, db)



def get_booking(booking_id, user, db):
    booking = booking_repository.get_booking_by_id(booking_id, user, db)
    if not booking:
        raise HTTPException(status_code=404, detail="not found")

    return booking



def delete_booking(booking_id: int, user: Users, db:Session):
    booking = booking_repository.get_booking_by_id(booking_id, user, db)

    if not booking:
        raise HTTPException(status_code=404, detail="not found")

    booking_repository.delete_booking(booking, db)



def check_expired_booking(event_id:int, seat_id: int, db:Session):
    current_time = datetime.now(UTC)
    return booking_repository.check_expired_booking(event_id, seat_id, db, current_time, status = "held")