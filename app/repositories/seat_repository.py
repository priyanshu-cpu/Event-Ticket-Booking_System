from sqlalchemy.orm import Session
from app.models.seats import Seat
from app.schemas.seat import SeatBase



def get_seats(id: int, db:Session):
    return db.query(Seat).filter(Seat.venue_id == id).all()


def get_seat_by_id(seat_id: int, db:Session):
    return db.query(Seat).filter(Seat.id == seat_id).first()


def get_seat_for_update(seat_id: int, db: Session):
    return (
        db.query(Seat)
        .filter(Seat.id == seat_id)
        .with_for_update()
        .first()
    )