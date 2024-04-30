import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import decode_jwt
from src.auth.models import User
from src.database import db

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login/", auto_error=False
)


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


async def get_user_or_none(
    session: AsyncSession = Depends(db.scoped_session_dependency),
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        return None
    token_type = payload.get("type")
    user_id = payload.get("id")
    if token_type == "access_token":
        stmt = select(User).where(User.id == user_id)
        user: None | User = await session.scalar(stmt)
        await session.close()
        if user:
            return user
    return None