from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import user_repository
from app.core.security import generate_password_hash
from app.core.security import verify_password, create_token
from app.models.user import Users


from app.schemas.user import UserBase, UserLoginSchema



def create_user(db:Session, user:UserBase):

    exsiting_user = user_repository.get_user_by_name(user.name, db)
    if exsiting_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    if user.email:
        existing_email = user_repository.get_user_by_email(user.email, db)
        if existing_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already exists")

    pass_hash = generate_password_hash(user.password)

    return user_repository.create_user(user, pass_hash, db)



def login_user(db:Session, payload:UserLoginSchema):
    existing_user = user_repository.get_user_by_name(payload.username, db)

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    if not verify_password(payload.password, existing_user.pasword_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    token = create_token({
        "sub" : str(existing_user.id)
    })
    return token



def get_user_info(user:Users, db:Session):
    return user_repository.get_user_by_id(user.id, db)



def update_user(user:Users, form_data: UserBase, db:Session):
    password_hash = generate_password_hash(form_data.password)

    return user_repository.update_user(user.id, form_data, password_hash,db)



def delete_user(db:Session, user:Users):
    return user_repository.delete_user(db, user)