from datetime import datetime
from decimal import Decimal
from typing import Literal, get_args
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum


from src.database import Base


class Check(Base):

    date_created: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    creator = relationship("User", back_populates="check")
    product = relationship("Product", back_populates="check")
    payment = relationship("Payment", back_populates="check")

    @property
    def total_amount(self):
        return sum(p.amount * p.price for p in self.product)


class Payment(Base):
    TYPE = Literal["cash", "cashless"]
    payment_type = Enum(
        *get_args(TYPE),
        name="payment_type",
        create_constraint=True,
        validate_strings=True,
    )
    type: Mapped[TYPE] = mapped_column(payment_type)
    amount: Mapped[Decimal] = mapped_column(nullable=False)
    check_id: Mapped[int] = mapped_column(ForeignKey("check.id"), nullable=True)
    check = relationship("Check", back_populates="payment")

    def __str__(self):
        return self.type


class Product(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    check_id: Mapped[int] = mapped_column(ForeignKey("check.id"), nullable=True)
    check = relationship("Check", back_populates="product")

    def __str__(self):
        return self.name
