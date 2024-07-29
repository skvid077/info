import json
import os

from sqlalchemy import select, update, insert, delete

from typing import Unpack

from schemas import s_pydantic, s_kwargs

import database.models as models

from database.json_models import get_path as get_path_json_models


class Variant:

    @staticmethod
    async def read() -> dict[int, list[int]]:
        with open(file=os.path.join(get_path_json_models(), 'variants.json'),
                  mode='r',
                  encoding='utf-8') as f:
            data: dict[int, list[int]] = {int(key): value for key, value in json.loads(f.read()).items()}
        return data

    @staticmethod
    async def write(data: dict[int, list[int]]):
        with open(file=os.path.join(get_path_json_models(), 'variants.json'),
                  mode='w',
                  encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    async def check(variant_id: int) -> bool:
        async with models.async_session_factory() as session:
            query = select(models.Variant).filter_by(id=variant_id)
            result = await session.execute(query)
        return bool(result.scalars().all())

    @staticmethod
    async def check_author(author_id: int, variant_id: int) -> bool:
        async with models.async_session_factory() as session:
            query = select(models.Variant.author_id).filter_by(id=variant_id)
            result = await session.execute(query)
        return result.scalars().one() == author_id

    @staticmethod
    async def show(variant_id: int) -> s_pydantic.Variant:
        from database.queries.queries_to_db.task import Task
        async with models.async_session_factory() as session:
            query = select(models.Variant).filter_by(id=variant_id)
            result = await session.execute(query)
        data: dict[int, list[int]] = await Variant.read()
        result = s_pydantic.Variant.model_validate(result.scalars().one(), from_attributes=True)
        result.tasks = [await Task.show(task_id) for task_id in data[variant_id]]
        return result

    @staticmethod
    async def num() -> int:
        async with models.async_session_factory() as session:
            query = select(models.Variant.id)
            result = await session.execute(query)
        return max(result.scalars().all() + [0])

    @staticmethod
    async def nums() -> list[int]:
        async with models.async_session_factory() as session:
            query = select(models.Variant.id)
            result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def add(**values: Unpack[s_kwargs.Variant]):
        async with models.async_session_factory() as session:
            query = insert(models.Variant).values(
                values
            )
            await session.execute(query)
            await session.commit()
        data: dict[int, list[int]] = await Variant.read()
        data[await Variant.num()] = []
        await Variant.write(data)

    @staticmethod
    async def del_(variant_id: int):
        async with models.async_session_factory() as session:
            query = delete(models.Variant).filter_by(id=int(variant_id))
            await session.execute(query)
            await session.commit()
        data: dict[int, list[int]] = await Variant.read()
        del data[variant_id]
        await Variant.write(data)

    @staticmethod
    async def update_minus_task(variant_id: int, task_id: int):
        data: dict[int, list[int]] = await Variant.read()
        data[variant_id].remove(task_id)
        await Variant.write(data)

    @staticmethod
    async def update_plus_task(variant_id: int, task_id: int):
        data: dict[int, list[int]] = await Variant.read()
        data[variant_id].append(task_id)
        await Variant.write(data)

    @staticmethod
    async def update(**values: Unpack[s_kwargs.Variant]):
        variant_id: int = values.pop('id')
        async with models.async_session_factory() as session:
            query = update(models.Variant).values(
                values
            ).filter_by(id=variant_id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def check_task_in(variant_id: int, task_id: int) -> bool:
        data: dict[int, list[int]] = await Variant.read()
        return task_id in data[variant_id]
