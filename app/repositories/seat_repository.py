from sqlalchemy.orm import Session
from app.models.seats import Seat
from app.schemas.seat import SeatBase



def get_seats(id: int, db:Session):
    return db.query(Seat).filter(Seat.venue_id == id).all()
