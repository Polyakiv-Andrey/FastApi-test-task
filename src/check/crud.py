from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

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
