import asyncio

from database.models.base import async_engine, async_session_factory, Base
from database.models.variant import Variant
from database.models.user import User
from database.models.task import Task


async def main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
