from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.bookings import BookingCreate, BookingResponse, BookingStatus
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services import booking as booking_service
from app.core.exceptions import NotFound, Unauthorized, DoesntExist
from app.models.user import User 
from app.utils.security import get_current_user


router = APIRouter(prefix='/api/bookings', tags=['Booking'])


DbSession = Annotated[AsyncSession, Depends(get_db)]

CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[BookingResponse])
async def get_bookings(db: DbSession, user: CurrentUser):
    return await booking_service.get_bookings(db, user)


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking_by_id(booking_id: int, db: DbSession, user: CurrentUser):
    try:
        booking = await booking_service.get_booking_by_id(booking_id, db, user)
    except NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Booking not found')
    return booking