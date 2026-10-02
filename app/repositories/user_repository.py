from sqlalchemy.orm import Session
from app.models.user import Users
from app.schemas.user import UserBase



def create_user(user: UserBase, pass_hash, db:Session):
    new_user = Users(name = user.name, email = user.email,pasword_hash = pass_hash )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



def get_user_by_name(name: str, db:Session):
    return db.query(Users).filter(Users.name == name).first()



def get_user_by_email(email:str, db:Session):
    return db.query(Users).filter(Users.email == email).first()



def get_user_by_id(user_id: int, db:Session):
    return db.get(Users, user_id)