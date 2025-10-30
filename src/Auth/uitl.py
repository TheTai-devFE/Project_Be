from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import uuid
from src.db.config import Config
import logging

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_hashed_password(password: str) -> str:
    hash = password_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
) -> str:
    payload = {
        "user": user_data,
        "exp": datetime.now()
        + (expiry if expiry is not None else timedelta(minutes=3690)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as jwte:
        logging.exception("JWT Decode Error: %s", str(jwte))
        return None
    except Exception as e:
        logging.exception("Unexpected Error during JWT Decode: %s", str(e))
        return None
