from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):

    name: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    username = Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    data_created: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self) -> str:
        return self.username
