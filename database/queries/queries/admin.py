from typing import Optional

from database.queries import queries_to_db


class Admin:

    @staticmethod
    async def check(telegram_id: int) -> Optional[bool]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.Admin.check(telegram_id=telegram_id)

    @staticmethod
    async def add(telegram_id: int) -> Optional[bool]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        if await queries_to_db.Admin.check(telegram_id=telegram_id):
            return False
        await queries_to_db.Admin.add(telegram_id=telegram_id)
        return True

    @staticmethod
    async def del_(telegram_id: int) -> Optional[bool]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        if not await queries_to_db.Admin.check(telegram_id=telegram_id):
            return False
        await queries_to_db.Admin.del_(telegram_id=telegram_id)
        return True
