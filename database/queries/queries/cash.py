from typing import Optional

from database.queries import queries_to_db


class Cash:
    @staticmethod
    async def show(telegram_id: int) -> Optional[int]:
        if not await queries_to_db.User.show(telegram_id=telegram_id):
            return None
        return await queries_to_db.Cash.show(telegram_id=telegram_id)

    @staticmethod
    async def plus(telegram_id: int, cash: int) -> Optional[bool]:
        if not await queries_to_db.User.show(telegram_id=telegram_id):
            return None
        await queries_to_db.Cash.plus(telegram_id=telegram_id, cash=cash)
        return True

    @staticmethod
    async def minus(telegram_id: int, cash: int) -> Optional[bool]:
        if not await queries_to_db.User.show(telegram_id=telegram_id):
            return None
        if await queries_to_db.Cash.show(telegram_id=telegram_id) < cash:
            return False
        await queries_to_db.Cash.plus(telegram_id=telegram_id, cash=cash)
        return True
