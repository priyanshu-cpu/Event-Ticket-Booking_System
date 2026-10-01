from sqlalchemy.orm import Session
from app.models.user import Users



def create_user(user: Users, db:Session):
    


    db.add(user)
    db.commit()
    db.refresh(user)

    return