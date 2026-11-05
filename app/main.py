from fastapi import FastAPI
from app.api.routers.users import router as user_router
from app.api.routers.venue import router as venue_router
from app.api.routers.event import router as event_router
from app.api.routers.seats import router as seat_router



app = FastAPI(title="Event ticket booking system")

app.include_router(user_router)
app.include_router(venue_router)
app.include_router(event_router)
app.include_router(seat_router)