from sqlalchemy import select, update, insert, delete

from typing import Unpack

from schemas import s_pydantic, s_kwargs

import database.models as models


class Task:

    @staticmethod
    async def add(**values: Unpack[s_kwargs.Task]):
        async with models.async_session_factory() as session:
            query = insert(models.Task).values(
                values
            )
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def update(**values: Unpack[s_kwargs.Task]):
        task_id = values.pop('id')
        async with models.async_session_factory() as session:
            query = update(models.Task).filter_by(id=task_id).values(
                values
            )
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def del_(task_id: int):
        from database.queries.queries_to_db.variant import Variant
        async with models.async_session_factory() as session:
            query = delete(models.Task).filter_by(id=task_id)
            await session.execute(query)
            await session.commit()
        data: dict[int, list[int]] = await Variant.read()
        for key in data:
            while task_id in data[key]:
                data[key].remove(task_id)
        await Variant.write(data)

    @staticmethod
    async def show(task_id: int) -> s_pydantic.Task:
        async with models.async_session_factory() as session:
            query = select(models.Task).filter_by(id=task_id)
            result = await session.execute(query)
            task = result.scalars().one()
        return s_pydantic.Task.model_validate(task, from_attributes=True)

    @staticmethod
    async def check(task_id: int) -> bool:
        async with models.async_session_factory() as session:
            query = select(models.Task).filter_by(id=task_id)
            result = await session.execute(query)
        return bool(result.scalars().all())

    @staticmethod
    async def check_author(author_id: int, task_id: int) -> bool:
        async with models.async_session_factory() as session:
            query = select(models.Task.author_id).filter_by(id=task_id)
            result = await session.execute(query)
        return result.scalars().one() == author_id

    @staticmethod
    async def nums() -> list[int]:
        async with models.async_session_factory() as session:
            query = select(models.Variant.id)
            result = await session.execute(query)
        return result
