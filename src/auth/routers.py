from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.crud import create_user, validate_auth_user
from src.auth.jwt import create_access_token_from_refresh
from src.auth.schemas import UserRegistrationsSchema, JWTTokens, AccessToken
from src.database import db

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/registration/")
async def user_registration(
        user: UserRegistrationsSchema,
        session: AsyncSession = Depends(db.scoped_session_dependency)
) -> JWTTokens:
    response = await create_user(session=session, user=user)
    return response


@auth_router.post("/login/")
async def login(
        session: AsyncSession = Depends(db.scoped_session_dependency),
        username: str = Form(),
        password: str = Form(),
) -> JWTTokens:
    response = await validate_auth_user(session, username, password)
    return response


@auth_router.post("/refresh-token/")
async def refreshing_token(
        refresh_token: str = Form(),
) -> AccessToken:
    response = await create_access_token_from_refresh(refresh_token=refresh_token)
    return response
