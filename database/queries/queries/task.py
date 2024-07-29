from schemas import s_pydantic, s_kwargs

from typing import Unpack, Optional

from database.queries import queries_to_db

from database.tasks import s3_client


class Task:

    @staticmethod
    async def add(**values: Unpack[s_kwargs.Task]) -> bool:
        await queries_to_db.Task.add(**values)
        return True

    @staticmethod
    async def update(**values: Unpack[s_kwargs.Task]) -> Optional[bool]:
        if not await queries_to_db.Task.check(task_id=values['id']):
            return None
        await queries_to_db.Task.update(**values)
        return True

    @staticmethod
    async def del_(task_id: int) -> Optional[bool]:
        if not await queries_to_db.Task.check(task_id=task_id):
            return None
        await queries_to_db.Task.del_(task_id=task_id)
        s3_client.delete_file(file_url=f'{task_id}_task.zip')
        return True

    @staticmethod
    async def show(task_id: int) -> Optional[s_pydantic.Task]:
        if not await queries_to_db.Task.check(task_id=task_id):
            return None
        return await queries_to_db.Task.show(task_id=task_id)

    @staticmethod
    async def check(task_id: int) -> bool:
        return await queries_to_db.Task.check(task_id=task_id)

    @staticmethod
    async def check_author(author_id: int, task_id: int) -> Optional[bool]:
        if not await queries_to_db.Task.check(task_id=task_id):
            return None
        return await queries_to_db.Task.check_author(author_id=author_id, task_id=task_id)

    @staticmethod
    async def nums() -> list[int]:
        return await queries_to_db.Task.nums()
