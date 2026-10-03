from fastapi import APIRouter, Depends
from app.schemas.seat import SeatOut, SeatBase, SeatCreatResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import Users
from app.models.seats import Seat
from app.api.deps import get_current_user
from app.services import seat_service





router = APIRouter(prefix="/seat", tags=["Seat"])



router.get("/seat", response_model=SeatOut)
def get_seat(db:Session = Depends(get_db), user:Users = Depends(get_current_user)):
    return 