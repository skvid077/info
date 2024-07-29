from sqlalchemy import select, update

import database.models as models


class Cash:
    @staticmethod
    async def show(telegram_id: int) -> int:
        async with models.async_session_factory() as session:
            query = select(models.User.cash).filter_by(telegram_id=telegram_id)
            result = await session.execute(query)
            cash = result.scalars().one()
        return cash

    @staticmethod
    async def plus(telegram_id: int, cash: int):
        async with models.async_session_factory() as session:
            cash += Cash.show(telegram_id)
            query = update(models.User).values(cash=cash).filter_by(
                telegram_id=telegram_id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def minus(telegram_id: int, cash: int):
        async with models.async_session_factory() as session:
            query = update(models.User).values(cash=-cash).filter_by(
                telegram_id=telegram_id)
            await session.execute(query)
            await session.commit()
