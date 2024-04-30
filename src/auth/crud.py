from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import encode_jwt
from src.auth.models import User
from src.auth.schemas import UserRegistrationsSchema
from src.auth.utils import hash_password, validate_password


async def create_user(session: AsyncSession, user: UserRegistrationsSchema):
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )
    new_user = User(
        name=user.name,
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    session.add(new_user)
    await session.commit()
    tokens = encode_jwt({"id": new_user.id})
    return tokens


async def validate_auth_user(
        session: AsyncSession,
        username: str,
        password: str,
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    stmt = select(User).where(User.username == username)
    user: None | User = await session.scalar(stmt)
    if not user:
        await session.close()
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_password=user.hashed_password,
    ):
        await session.close()
        raise unauthed_exc

    if not user.is_active:
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    await session.close()
    tokens = encode_jwt({"id": user.id})
    return tokens
