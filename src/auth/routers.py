from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.crud import create_user
from src.auth.schemas import UserRegistrationsSchema, JWTTokens
from src.database import db

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/registration/")
async def user_registration(
        user: UserRegistrationsSchema,
        session: AsyncSession = Depends(db.scoped_session_dependency)
) -> JWTTokens:
    response = await create_user(session=session, user=user)
    return response
