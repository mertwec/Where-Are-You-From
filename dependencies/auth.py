from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from crud.user import get_user
from dependencies.database import AsyncSession, get_session
from models import User
from settings import logger, settings_app

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    if not expires_delta:
        expires_delta = timedelta(minutes=15)
    expire = datetime.now(timezone.utc) + expires_delta
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data, settings_app.SECRET_KEY, algorithm=settings_app.ALGORITHM
    )
    return encoded_jwt


def raise_credentials_exception(message: str = "Could not validate credentials"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"Authenticate": "Bearer"},
    )


def decode_access_token(token):
    try:
        payload = jwt.decode(
            token,
            settings_app.SECRET_KEY,
            algorithms=[settings_app.ALGORITHM],
            options={"verify_exp": True},
        )
        return payload

    except jwt.ExpiredSignatureError:
        logger.debug("Token has expired.")
        raise_credentials_exception("Token has expired.")
    except jwt.PyJWTError as e:
        logger.debug(f"Token decoding error: {e}")
        raise_credentials_exception(f"Token decoding error: {e}")


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> User:
    data_user = decode_access_token(token)

    if not data_user:
        raise_credentials_exception()
    current_user = await get_user(session, data_user.get("sub"))
    return current_user
