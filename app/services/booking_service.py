from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import booking_repository
from app.repositories import event_repository
from app.repositories import seat_repository
from app.schemas.booking import BookingBase
from app.models.user import Users
from app.models.bookings import Booking




def create_booking(
        form_data: BookingBase,
        user:Users,
        db:Session
):
    event = event_repository.get_event_by_id(form_data.event_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")

    seat = seat_repository.get_seat_by_id(form_data.seat_id, db)
    if not seat:
        raise HTTPException(status_code=404, detail="seat not found")

    if not seat.venue_id == event.venue_id:
        raise HTTPException(status_code=400, detail="Seat does not belogs to the event!")

    booking = booking_repository.get_booking_by_event_and_seat(form_data.event_id, form_data.seat_id, db)
    if booking:
        if not booking.status == "available":
            raise HTTPException(status_code=400, detail="seat is not available")

    new_booking = booking_repository.create_booking(form_data, user, db)
    return new_booking



def get_bookings(user:Users, db:Session):
    return booking_repository.get_bookings(user, db)



def get_booking(booking_id, user, db):
    booking = booking_repository.get_booking_by_id(booking_id, user, db)
    if not booking:
        raise HTTPException(status_code=404, detail="not found")

    return booking