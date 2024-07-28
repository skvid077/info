import json

from sqlalchemy import select, update, insert, delete
from sqlalchemy.orm import selectinload

from typing import Unpack

from schemas import s_pydantic, s_kwargs

import database.models as models


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
    async def show_friends(telegram_id: int) -> s_pydantic.User_friends:
        async with models.async_session_factory() as session:
            query = select(models.User).filter_by(telegram_id=telegram_id)
            result = await session.execute(query)
        result = result.unique().scalars().one()
        user = s_pydantic.User_friends.model_validate(result, from_attributes=True)
        user.friends = [await User.show(friend) for friend in await Friends.show_friends(telegram_id)]
        return user

    @staticmethod
    async def show_friends_request_from_me(telegram_id: int) -> s_pydantic.User_friends_request_from_me:
        async with models.async_session_factory() as session:
            query = select(models.User).filter_by(telegram_id=telegram_id)
            result = await session.execute(query)
        result = result.unique().scalars().one()
        user = s_pydantic.User_friends_request_from_me.model_validate(result, from_attributes=True)
        user.friends_request_from_me = [await User.show(friend) for friend in
                                        await Friends.show_friends_request_from_me(telegram_id)]
        return user

    @staticmethod
    async def show_friends_request_for_me(telegram_id: int) -> s_pydantic.User_friends_request_for_me:
        async with models.async_session_factory() as session:
            query = select(models.User).filter_by(telegram_id=telegram_id)
            result = await session.execute(query)
        result = result.unique().scalars().one()
        user = s_pydantic.User_friends_request_for_me.model_validate(result, from_attributes=True)
        user.friends_request_for_me = [await User.show(friend) for friend in
                                       await Friends.show_friends_request_for_me(telegram_id)]
        return user

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
            "variants": [],
            "tasks": []
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


class Cash:
    @staticmethod
    async def show(telegram_id: int) -> int:
        async with models.async_session_factory() as session:
            query = select(models.User.cash).filter_by(telegram_id=telegram_id)
            result = await session.execute(query)
            cash = result.scalars().one()
        return cash

    @staticmethod
    async def plus(telegram_id: int, cash: int):
        async with models.async_session_factory() as session:
            cash += Cash.show(telegram_id)
            query = update(models.User).values(cash=cash).filter_by(
                telegram_id=telegram_id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def minus(telegram_id: int, cash: int):
        async with models.async_session_factory() as session:
            query = update(models.User).values(cash=-cash).filter_by(
                telegram_id=telegram_id)
            await session.execute(query)
            await session.commit()


class Friends:

    @staticmethod
    async def read() -> dict[int, dict[str, list[int]]]:
        with open(file='C:\\work\\project\\info\\database\\json_models\\friends.json', mode='r', encoding='utf-8') as f:
            data: dict[int, dict[str, list[int]]] = {int(key): value for key, value in json.loads(f.read()).items()}
        await Friends.write(data)
        return data

    @staticmethod
    async def write(data: dict[int, dict[str, list[int]]]):
        with open(file='C:\\work\\project\\info\\database\\json_models\\friends.json', mode='w', encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    async def check_friend(friend1: int, friend2: int) -> bool:
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        return friend1 in data[friend2]['friends']

    @staticmethod
    async def check_request_from_me(sender_id: int, addressee_id: int) -> bool:
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        return addressee_id in data[sender_id]['friends_request_from_me']

    @staticmethod
    async def check_black_list(sender_id: int, addressee_id: int) -> bool:
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        return addressee_id in data[sender_id]['black_list']

    @staticmethod
    async def add_friend(sender_id: int, addressee_id: int):
        await Friends.del_request_from_me(addressee_id, sender_id)
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data[addressee_id]['friends'].append(sender_id)
        data[sender_id]['friends'].append(addressee_id)
        await Friends.write(data)

    @staticmethod
    async def add_request_for_me(sender_id: int, addressee_id: int):
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data[addressee_id]['friends_request_for_me'].append(sender_id)
        await Friends.write(data)

    @staticmethod
    async def add_request_from_me(sender_id: int, addressee_id: int):
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data[sender_id]['friends_request_from_me'].append(addressee_id)
        await Friends.write(data)

    @staticmethod
    async def add_black_list(sender_id: int, addressee_id: int):
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data[sender_id]['black_list'].append(addressee_id)
        await Friends.write(data)

    @staticmethod
    async def del_friend(sender_id: int, addressee_id: int):
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data[addressee_id]['friends'].remove(sender_id)
        data[sender_id]['friends'].remove(addressee_id)
        await Friends.write(data)

    @staticmethod
    async def del_request_for_me(sender_id: int, addressee_id: int):
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data[addressee_id]['friends_request_for_me'].remove(sender_id)
        await Friends.write(data)

    @staticmethod
    async def del_request_from_me(sender_id: int, addressee_id: int):
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data[sender_id]['friends_request_from_me'].remove(addressee_id)
        await Friends.write(data)

    @staticmethod
    async def del_black_list(sender_id: int, addressee_id: int):
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        data[sender_id]['black_list'].remove(addressee_id)
        await Friends.write(data)

    @staticmethod
    async def show_friends(telegram_id: int) -> list[int]:
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        return data[telegram_id]['friends']

    @staticmethod
    async def show_friends_request_for_me(telegram_id: int) -> list[int]:
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        return data[telegram_id]['friends_request_for_me']

    @staticmethod
    async def show_friends_request_from_me(telegram_id: int) -> list[int]:
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        return data[telegram_id]['friends_request_from_me']

    @staticmethod
    async def show_black_list(telegram_id: int) -> list[int]:
        data: dict[int, dict[str, list[int]]] = await Friends.read()
        return data[telegram_id]['black_list']


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


class Variant:

    @staticmethod
    async def read() -> dict[int, list[int]]:
        with open(file='C:\\work\\project\\info\\database\\json_models\\variants.json',
                  mode='r',
                  encoding='utf-8') as f:
            data: dict[int, list[int]] = {int(key): value for key, value in json.loads(f.read()).items()}
        return data

    @staticmethod
    async def write(data: dict[int, list[int]]):
        with open(file='C:\\work\\project\\info\\database\\json_models\\variants.json',
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
