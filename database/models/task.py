import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, text

from database.models.base import Base, str_50

from schemas import s_enumeration


class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey(column='user.telegram_id', ondelete='CASCADE'), nullable=False)
    num: Mapped[int] = mapped_column(nullable=False)
    ans: Mapped[str_50] = mapped_column(nullable=False)
    extend_ans: Mapped[str_50] = mapped_column(nullable=False)
    verif: Mapped[bool] = mapped_column(nullable=False, server_default=text('false'))
    complexity: Mapped[s_enumeration.Complexity] = mapped_column(nullable=True)
    at_create: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default=func.now())
    author: Mapped['User'] = relationship(
        back_populates='tasks'
    )
