from fastapi import Depends, HTTPException
from app.core.security import verify_token, credentials_exception
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.user import Users




def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        user_id = int(payload["sub"])
    except (TypeError, KeyError, ValueError):
        raise credentials_exception
    user = db.get(Users, user_id)
    if user is None:
        raise credentials_exception
    return user
