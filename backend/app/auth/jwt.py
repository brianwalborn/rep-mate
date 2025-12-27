from datetime import datetime, timedelta
from jose import jwt
from os import getenv

ACCESS_TOKEN_EXPIRY_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRY_MINUTES", "120"))
ALGORITHM = "HS256"
JWT_ENCODE_SECRET_KEY = getenv("JWT_ENCODE_SECRET_KEY", "dev-secret-change-me")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, JWT_ENCODE_SECRET_KEY, algorithm=ALGORITHM)
