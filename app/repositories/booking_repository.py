from sqlalchemy.orm import Session
from app.models.bookings import Booking
from app.schemas.booking import BookingBase
from app.models.user import Users
from app.models.seats import Seat
from app.models.event import Event
from app.models.venue import Venue


def create_booking(
    form_data: BookingBase,
    user: Users,
    db: Session,
    expires,
    status: str = "held",
    commit: bool = True,
):
    new_booking = Booking(
        user_id=user.id,
        event_id=form_data.event_id,
        seat_id=form_data.seat_id,
        status=status,
        hold_expires_at=expires,
    )

    db.add(new_booking)
    db.flush()
    if commit:
        db.commit()
        db.refresh(new_booking)

    return new_booking


def get_booking_by_event_and_seat(event_id: int, seat_id: int, db: Session):
    return (
        db.query(Booking)
        .filter(Booking.event_id == event_id, Booking.seat_id == seat_id, Booking.status.in_(["held", "confirmed"]))
        .first()
    )


def get_bookings(user: Users, db: Session):
    return db.query(Booking).filter(Booking.user_id == user.id).all()


def get_booking_by_id(booking_id: int, user: Users, db: Session):
    return (
        db.query(Booking)
        .filter(Booking.id == booking_id, Booking.user_id == user.id)
        .first()
    )


def delete_booking(booking, db: Session):

    db.delete(booking)
    db.commit()
    return {}


def get_active_booking(event_id: int, seat_id: int, db: Session):
    booking = (
        db.query(Booking)
        .filter(
            Booking.event_id == event_id,
            Booking.seat_id == seat_id,
            Booking.status.in_(["held", "confirmed"]),
        )
        .first()
    )

    return booking


def check_expired_booking(event_id:int, seat_id: int, db: Session, current_time, status: str):
    update_count = (
        db.query(Booking)
        .filter(Booking.event_id == event_id, Booking.seat_id == seat_id, Booking.status == status, Booking.hold_expires_at <= current_time)
        .update({Booking.status: "expired"}, synchronize_session=False)
    )

    return update_count



def update_booking_status(booking:Booking, status:str, db:Session):
    booking.status = status
    db.flush()
    return booking