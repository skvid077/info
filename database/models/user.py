from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text

from database.models.base import Base, str_50


class User(Base):
    __tablename__ = 'user'
    telegram_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    username: Mapped[str_50] = mapped_column(nullable=True)
    cash: Mapped[int] = mapped_column(nullable=False, server_default=text('0'))
    is_admin: Mapped[bool] = mapped_column(nullable=False, server_default=text('false'))
    tasks: Mapped[list['Task']] = relationship(
        back_populates='author'
    )
    variants: Mapped[list['Variant']] = relationship(
        back_populates='author'
    )
