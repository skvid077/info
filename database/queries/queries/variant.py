from schemas import s_pydantic, s_kwargs

from typing import Unpack, Optional

from database.queries import queries_to_db

from database.tasks import s3_client


class Variant:

    @staticmethod
    async def check(variant_id: int) -> bool:
        return await queries_to_db.Variant.check(variant_id=variant_id)

    @staticmethod
    async def check_author(author_id: int, variant_id: int) -> Optional[bool]:
        if not await queries_to_db.User.check(telegram_id=author_id):
            return None
        return await queries_to_db.Variant.check_author(author_id=author_id, variant_id=variant_id)

    @staticmethod
    async def show(variant_id: int) -> Optional[s_pydantic.Variant]:
        if not await queries_to_db.Variant.check(variant_id=variant_id):
            return None
        return await queries_to_db.Variant.show(variant_id=variant_id)

    @staticmethod
    async def add(**values: Unpack[s_kwargs.Variant]) -> bool:
        await queries_to_db.Variant.add(**values)
        return True

    @staticmethod
    async def nums() -> list[int]:
        return await queries_to_db.Variant.nums()

    @staticmethod
    async def del_(variant_id: int) -> Optional[bool]:
        if not queries_to_db.Variant.check(variant_id=variant_id):
            return None
        await queries_to_db.Variant.del_(variant_id=variant_id)
        await s3_client.delete_file(file_url=f'{variant_id}_variant.zip')
        return True

    @staticmethod
    async def update_minus_task(variant_id: int, task_id: int) -> Optional[bool]:
        if not await queries_to_db.Variant.check(variant_id=variant_id):
            return None
        if not await queries_to_db.Variant.check_task_in(variant_id=variant_id, task_id=task_id):
            return False
        await queries_to_db.Variant.update_minus_task(variant_id=variant_id, task_id=task_id)
        return True

    @staticmethod
    async def update_plus_task(variant_id: int, task_id: int) -> Optional[bool]:
        if not await queries_to_db.Variant.check(variant_id=variant_id):
            return None
        await queries_to_db.Variant.update_plus_task(variant_id=variant_id, task_id=task_id)
        return True

    @staticmethod
    async def update(**values: Unpack[s_kwargs.Variant]) -> Optional[bool]:
        if not await queries_to_db.Variant.check(variant_id=values['id']):
            return None
        await queries_to_db.Variant.update(**values)
        return True

    @staticmethod
    async def check_task_in(variant_id: int, task_id: int) -> bool:
        return await queries_to_db.Variant.check_task_in(variant_id=variant_id, task_id=task_id)
