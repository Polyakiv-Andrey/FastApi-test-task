from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException,status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.utils import get_user_or_none
from src.check.check_text import adjust_string, center_text
from src.check.crud import create_new_check, get_check_from_bd, get_list_checks, get_check_creator

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


@check_router.get("/get-check/{check_id}")
async def get_check_by_id(
        check_id: int,
        session: AsyncSession = Depends(db.scoped_session_dependency),
        user: Optional[User] = Depends(get_user_or_none)
) -> CheckDetail:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    response = await get_check_from_bd(session=session, check_id=check_id)
    return response


@check_router.get("/get-my-checks/")
async def get_my_checks(
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        total_amount_min: Optional[float] = None,
        payment_type: Optional[str] = None,
        session: AsyncSession = Depends(db.scoped_session_dependency),
        user: Optional[User] = Depends(get_user_or_none),
        limit: int = 10,
        offset: int = 0,
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    response = await get_list_checks(
        session=session,
        user_id=user.id,
        limit=limit,
        offset=offset,
        payment_type=payment_type,
        total_amount_min=total_amount_min,
        date_from=date_from,
        date_to=date_to
    )
    return response


@check_router.get("/text-check/{check_id}/")
async def get_text_file(
        check_id: int,
        max_line_length: int = 50,
        session: AsyncSession = Depends(db.scoped_session_dependency),
):
    check_data = await get_check_from_bd(session=session, check_id=check_id)
    creator = await get_check_creator(session=session, check_id=check_id)

    text_content = ""
    header = f"ФОП {creator}"

    text_content += center_text(header, max_line_length)

    text_content += "\n" + max_line_length * "=" + "\n"

    for product in check_data["products"]:
        quantity_price_line = f"{product['quantity']:.2f} x {product['price']:.2f}"
        name_total_line = f"{product['name']: <25} {product['total']:.2f}"

        quantity_price_lines = [quantity_price_line[i:i + max_line_length] for i in
                                range(0, len(quantity_price_line), max_line_length)]
        name_total_lines = [name_total_line[i:i + max_line_length] for i in
                            range(0, len(name_total_line), max_line_length)]

        for line in quantity_price_lines:
            text_content += line + "\n"
        for line in name_total_lines:
            text_content += line + "\n"
        text_content += "-" * max_line_length + "\n"

    text_content += adjust_string(f"СУМА {check_data['total']:.2f}", max_line_length) +"\n"
    text_content += adjust_string(
        f"{check_data['payment']['type']} {check_data['payment']['amount']:.2f}",
        max_line_length
    ) + "\n"
    text_content += adjust_string(f"Решта {check_data['rest']:.2f}", max_line_length) + "\n"
    text_content += max_line_length * "=" + "\n"
    text_content += center_text(f"{check_data['created_at']}", max_line_length) + "\n"
    text_content += center_text("Дякуємо за покупку!\n", max_line_length)
    response = Response(content=text_content, media_type="text/plain")
    response.headers["Content-Disposition"] = "attachment; filename=check.txt"

    return response
