from typing import Optional

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.utils import get_user_or_none
from src.check.crud import create_new_check
from src.check.schemas import CheckCreate, CheckDetail
from src.database import db

check_router = APIRouter(prefix="/check", tags=["Check"])


@check_router.post("/create-check/")
async def create_check(
        check: CheckCreate,
        session: AsyncSession = Depends(db.scoped_session_dependency),
        user: Optional[User] = Depends(get_user_or_none)
) -> CheckDetail:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    response = await create_new_check(session=session, check=check, user=user)
    return response
