from fastapi import APIRouter, Depends
from app.schemas.booking import BookingBase, BookingOut, BookingCreatedResponse

from app.models.user import Users
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.services import booking_service



router = APIRouter(prefix="/bookings", tags=["Bookings"])



@router.post("/", response_model=BookingCreatedResponse, status_code=201)
def create_booking(form_data: BookingBase, user:Users = Depends(get_current_user), db:Session = Depends(get_db)):
    new_booking = booking_service.create_booking(form_data, user, db)

    return{
        "message" : "booking created",
        "data": new_booking
    }



@router.get("/",response_model=list[BookingOut])
def get_bookings(user:Users = Depends(get_current_user), db:Session = Depends(get_db)):
    return booking_service.get_bookings(user, db)



@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, user:Users =Depends(get_current_user), db:Session = Depends(get_db)):
    return booking_service.get_booking(booking_id, user, db)


@router.delete("/{booking_id}", status_code=201)
def delete_booking(booking_id: int, user:Users =Depends(get_current_user), db:Session =Depends(get_db)):
    return booking_service.delete_booking(booking_id, user, db)