from fastapi import APIRouter, Depends
from app.schemas.seat import SeatOut, SeatBase, SeatCreatResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import Users
from app.models.seats import Seat
from app.api.deps import get_current_user
from app.services import seat_service
from app.schemas.seat import SeatBase, SeatOut, SeatCreatResponse





router = APIRouter(prefix="/venue", tags=["Seats"])



@router.get("/{id}/seat", response_model=list[SeatOut])
def get_seat(id: int, db:Session = Depends(get_db)):
    return seat_service.get_seats(id, db)
