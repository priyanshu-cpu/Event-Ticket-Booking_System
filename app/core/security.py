from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status



credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
            )



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



pwd_context = PasswordHash.recommended()



def generate_password_hash(password):
    return pwd_context.hash(password)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp" : expire
    })
    token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return token



def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if not payload.get("sub"):
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception