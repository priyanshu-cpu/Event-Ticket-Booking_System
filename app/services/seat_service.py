from sqlalchemy.orm import session
from fastapi import HTTPException, status
from app.repositories import seat_repository
from app.models.seats import Seat
from app.schemas.seat import SeatBase



def get_seats(db:session):
    return seat_repository.get_seats(db)