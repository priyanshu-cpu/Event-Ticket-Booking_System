from fastapi import FastAPI
from app.api.routes.venue import router as venue_router




app = FastAPI()



app.include_router(venue_router)