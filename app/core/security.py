from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash




pwd_context = PasswordHash()



def generate_password_hash(password):
    return pwd_context.hash(password)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



