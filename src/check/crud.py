from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, contains_eager, selectinload

from src.auth.models import User
from src.check.models import Check, Product, Payment
from src.check.schemas import CheckCreate


async def create_new_check(
        session: AsyncSession,
        check: CheckCreate,
        user: Optional[User]
):
    rest = check.payment.amount - sum([p.price * p.quantity for p in check.products])
    if rest < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough money!")
    db_check = Check(creator_id=user.id)
    session.add(db_check)
    await session.commit()
    await session.refresh(db_check)
    products = [
        Product(
            name=p.name,
            price=p.price,
            quantity=p.quantity,
            check_id=db_check.id
        )
        for p in check.products
    ]
    session.add_all(products)
    payment = Payment(
        type=check.payment.type,
        amount=check.payment.amount,
        check_id=db_check.id
    )
    session.add(payment)
    await session.commit()
    total = sum(p.price * p.quantity for p in products)
    return {
        "id": db_check.id,
        "products": [
            {
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity,
                "total": p.price * p.quantity
            } for p in products
        ],
        "payment": {
            "type": payment.type,
            "amount": float(payment.amount)
        },
        "total": total,
        "rest": payment.amount - total,
        "created_at": db_check.date_created,

    }


async def get_check_from_bd(
        check_id: int,
        session: AsyncSession
):
    stmt = select(Check).where(Check.id == check_id).options(
        joinedload(Check.product),
        joinedload(Check.payment)
    )
    result = await session.execute(stmt)
    check = result.scalars().first()

    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check not found!")
    total = sum(p.price * p.quantity for p in check.product)
    return {
        "id": check.id,
        "products": [
            {
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity,
                "total": p.price * p.quantity
            } for p in check.product
        ],
        "payment": {
            "type": check.payment[0].type,
            "amount": check.payment[0].amount
        },
        "total": total,
        "rest": check.payment[0].amount - total,
        "created_at": check.date_created,
    }


async def get_list_checks(
        session: AsyncSession,
        user_id: int,
        limit=10,
        offset=0,
        payment_type=None,
        total_amount_min=None,
        date_from=None,
        date_to=None
):
    stmt = select(Check).where(Check.creator_id == user_id).options(
        joinedload(Check.product),
        joinedload(Check.payment)
    )

    if date_from:
        stmt = stmt.where(Check.date_created >= date_from)
    if date_to:
        stmt = stmt.where(Check.date_created <= date_from)
    if total_amount_min is not None:
        pass
    if payment_type:
        stmt = select(Check).join(Check.payment).where(Payment.type == payment_type)
        stmt = stmt.options(contains_eager(Check.payment))

    subq = stmt.subquery()
    total_count_stmt = select(func.count()).select_from(subq)
    total_count = await session.execute(total_count_stmt)

    stmt = stmt.limit(limit).offset(offset)

    result = await session.execute(stmt)
    checks = result.unique().scalars().all()

    return {
        "total": total_count.scalar_one(),
        "result": [
            {
                "id": check.id,
                "products": [
                    {
                        "name": p.name,
                        "price": p.price,
                        "quantity": p.quantity,
                        "total": p.price * p.quantity
                    } for p in check.product
                ],
                "payment": {
                    "type": check.payment[0].type,
                    "amount": check.payment[0].amount
                },
                "total": sum(p.price * p.quantity for p in check.product),
                "rest": check.payment[0].amount - sum(p.price * p.quantity for p in check.product),
                "created_at": check.date_created,
            }
            for check in checks
        ]
    }


async def get_check_creator(
    check_id: int,
    session: AsyncSession
):
    result = await session.execute(select(Check).options(selectinload(Check.creator)).filter(Check.id == check_id))
    check = result.scalars().first()
    return check.creator.name


