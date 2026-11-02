import jwt
from datetime import datetime, UTC, timedelta
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token",
    headers={"WWW-Authenticate": "Bearer"},
)


oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/users/token")


password_hash = PasswordHash.recommended()



def generate_password_hash(password: str) -> str:
    return password_hash.hash(password)

DUMMY_HASH = generate_password_hash("dummy-password-for-timing")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp" : expire})

    token = jwt.encode(
        to_encode, settings.SECRET_KEY.get_secret_value(), settings.ALGORITHM
    )
    return token


async def verify_token(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
        )
        if not payload.get("sub"):
            raise credentials_exception
        return payload

    except jwt.InvalidTokenError:
        raise credentials_exception from None


async def get_current_user(
    payload: dict = Depends(verify_token), db: AsyncSession = Depends(get_db)
) -> User:
    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError, KeyError):
        raise credentials_exception from None
    
    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user
