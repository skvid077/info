from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload

from typing import Unpack

from schemas import s_pydantic, s_kwargs

import database.models as models

from database.queries.queries_to_db.task import Task
from database.queries.queries_to_db.friends import Friends
from database.queries.queries_to_db.variant import Variant


class User:

    @staticmethod
    async def check(telegram_id: int) -> bool:
        async with models.async_session_factory() as session:
            query = select(models.User).filter_by(telegram_id=telegram_id)
            flag = await session.execute(query)
            flag = flag.scalars().all()
        return bool(flag)

    @staticmethod
    async def show(telegram_id: int) -> s_pydantic.User:
        async with models.async_session_factory() as session:
            query = select(models.User).filter_by(telegram_id=telegram_id)
            result = await session.execute(query)
        result = result.unique().scalars().one()
        user = s_pydantic.User.model_validate(result, from_attributes=True)
        return user

    @staticmethod
    async def show_friends(telegram_id: int) -> list[s_pydantic.User]:
        return [await User.show(friend) for friend in await Friends.show_friends(telegram_id=telegram_id)]

    @staticmethod
    async def show_friends_request_from_me(telegram_id: int) -> list[s_pydantic.User]:
        return [await User.show(friend) for friend in
                await Friends.show_friends_request_from_me(telegram_id=telegram_id)]

    @staticmethod
    async def show_friends_request_for_me(telegram_id: int) -> list[s_pydantic.User]:
        return [await User.show(friend) for friend in
                await Friends.show_friends_request_for_me(telegram_id=telegram_id)]

    @staticmethod
    async def show_black_list(telegram_id: int) -> list[s_pydantic.User]:
        return [await User.show(friend) for friend in await Friends.show_black_list(telegram_id=telegram_id)]

    @staticmethod
    async def show_tasks(telegram_id: int) -> s_pydantic.User_tasks:
        async with models.async_session_factory() as session:
            query = select(models.User).filter_by(telegram_id=telegram_id).options(selectinload(models.User.tasks))
            result = await session.execute(query)
        result = result.unique().scalars().one()
        user = s_pydantic.User_tasks.model_validate(result, from_attributes=True)
        return user

    @staticmethod
    async def show_variants(telegram_id: int) -> s_pydantic.User_variants:
        async with models.async_session_factory() as session:
            query = select(models.User).filter_by(telegram_id=telegram_id).options(selectinload(models.User.variants))
            result = await session.execute(query)
        result = result.unique().scalars().one()
        user = s_pydantic.User_variants.model_validate(result, from_attributes=True)
        for i in range(len(user.variants)):
            user.variants[i] = await Variant.show(user.variants[i].id)
        return user

    @staticmethod
    async def add(**values: Unpack[s_kwargs.User]):
        async with models.async_session_factory() as session:
            query = insert(models.User).values(
                values
            )
            await session.execute(query)
            await session.commit()
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data[values['telegram_id']] = {
            "black_list": [],
            "friends_request_from_me": [],
            "friends_request_for_me": [],
            "friends": [],
            "variants_solved": [],
            "tasks_solved": []
        }
        await Friends.write(data)

    @staticmethod
    async def del_(telegram_id: int):
        async with models.async_session_factory() as session:
            query = delete(models.User).filter_by(telegram_id=telegram_id)
            await session.execute(query)
            await session.commit()
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data.pop(telegram_id)
        for user_key in data:
            for list_key in data[user_key]:
                if telegram_id in data[user_key][list_key]:
                    data[user_key][list_key].remove(telegram_id)
        await Friends.write(data)

    @staticmethod
    async def del_task_in_variants(telegram_id):
        user: s_pydantic.User_tasks = await User.show_tasks(telegram_id=telegram_id)
        data: dict[int, list[int]] = await Variant.read()
        for task in user.tasks:
            task = task.id
            for variant in data:
                while task in data[variant]:
                    data[variant].remove(task)
        await Variant.write(data)

    @staticmethod
    async def show_tasks_solved(telegram_id: int) -> list[s_pydantic.Task]:
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        return [await Task.show(task_id=task_id) for task_id in data[telegram_id]['tasks_solved']]

    @staticmethod
    async def show_variants_solved(telegram_id: int) -> list[s_pydantic.Variant]:
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        return [await Variant.show(variant_id=variant_id) for variant_id in data[telegram_id]['variants_solved']]
