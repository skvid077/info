import schemas.s_pydantic
from schemas import s_pydantic, s_kwargs

from typing import Unpack, Optional

from database.queries import queries_to_db


class User:

    @staticmethod
    async def check(telegram_id: int) -> bool:
        return await queries_to_db.User.check(telegram_id=telegram_id)

    @staticmethod
    async def show(telegram_id: int) -> Optional[s_pydantic.User]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.User.show(telegram_id=telegram_id)

    @staticmethod
    async def show_friends(telegram_id: int) -> Optional[list[s_pydantic.User]]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.User.show_friends(telegram_id=telegram_id)

    @staticmethod
    async def show_friends_request_from_me(telegram_id: int) -> Optional[list[s_pydantic.User]]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.User.show_friends_request_from_me(telegram_id=telegram_id)

    @staticmethod
    async def show_friends_request_for_me(telegram_id: int) -> Optional[list[s_pydantic.User]]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.User.show_friends_request_for_me(telegram_id=telegram_id)

    @staticmethod
    async def show_black_list(telegram_id: int) -> list[s_pydantic.User]:
        return await queries_to_db.User.show_black_list(telegram_id=telegram_id)

    @staticmethod
    async def show_tasks(telegram_id: int) -> Optional[s_pydantic.User_tasks]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.User.show_tasks(telegram_id=telegram_id)

    @staticmethod
    async def show_variants(telegram_id: int) -> Optional[s_pydantic.User_variants]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.User.show_variants(telegram_id=telegram_id)

    @staticmethod
    async def add(**values: Unpack[s_kwargs.User]) -> bool:
        if await queries_to_db.User.check(telegram_id=values['telegram_id']):
            return False
        await queries_to_db.User.add(**values)
        return True

    @staticmethod
    async def del_(telegram_id: int) -> bool:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return False
        await queries_to_db.User.del_task_in_variants(telegram_id=telegram_id)
        await queries_to_db.User.del_(telegram_id=telegram_id)
        return True

    @staticmethod
    async def show_tasks_solved(telegram_id: int) -> list[schemas.s_pydantic.Task]:
        return await queries_to_db.User.show_tasks_solved(telegram_id=telegram_id)

    @staticmethod
    async def show_variants_solved(telegram_id: int) -> list[schemas.s_pydantic.Variant]:
        return await queries_to_db.User.show_variants_solved(telegram_id=telegram_id)
