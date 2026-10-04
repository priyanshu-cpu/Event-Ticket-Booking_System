from sqlalchemy.orm import Session
from app.models.seats import Seat
from app.schemas.seat import SeatBase



def get_seats(db:Session):
    return db.query(Seat).all()