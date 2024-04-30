from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import encode_jwt
from src.auth.models import User
from src.auth.schemas import UserRegistrationsSchema
from src.auth.utils import hash_password


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
