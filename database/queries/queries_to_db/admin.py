from sqlalchemy import select, update

import database.models as models


class Admin:

    @staticmethod
    async def check(telegram_id: int) -> bool:
        async with models.async_session_factory() as session:
            query = select(models.User.is_admin).filter_by(telegram_id=telegram_id)
            flag = await session.execute(query)
            return bool(flag.scalars().all())

    @staticmethod
    async def add(telegram_id: int):
        async with models.async_session_factory() as session:
            query = update(models.User).values(admin=True).filter_by(telegram_id=telegram_id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def del_(telegram_id: int):
        async with models.async_session_factory() as session:
            query = update(models.User).values(admin=False).filter_by(telegram_id=telegram_id)
            await session.execute(query)
            await session.commit()
