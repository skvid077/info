from schemas import s_pydantic, s_kwargs

from typing import Unpack, Optional

import queries_to_db


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
    async def show_friends(telegram_id: int) -> Optional[s_pydantic.User_friends]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.User.show_friends(telegram_id=telegram_id)

    @staticmethod
    async def show_friends_request_from_me(telegram_id: int) -> Optional[s_pydantic.User_friends_request_from_me]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.User.show_friends_request_from_me(telegram_id=telegram_id)

    @staticmethod
    async def show_friends_request_for_me(telegram_id: int) -> Optional[s_pydantic.User_friends_request_for_me]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.User.show_friends_request_for_me(telegram_id=telegram_id)

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


class Friends:
    @staticmethod
    async def add_friend(sender_id: int, addressee_id: int) -> Optional[bool]:
        if not queries_to_db.User.check(telegram_id=addressee_id):
            return None
        if sender_id == addressee_id:
            return False
        if await queries_to_db.Friends.check_black_list(sender_id=sender_id, addressee_id=addressee_id):
            return False
        if await queries_to_db.Friends.check_black_list(sender_id=addressee_id, addressee_id=sender_id):
            return False
        if await queries_to_db.Friends.check_friend(friend1=sender_id, friend2=addressee_id):
            return False
        if await queries_to_db.Friends.check_request_from_me(sender_id=sender_id, addressee_id=addressee_id):
            return False
        if queries_to_db.Friends.check_request_from_me(sender_id=addressee_id, addressee_id=sender_id):
            await queries_to_db.Friends.add_friend(sender_id=sender_id, addressee_id=addressee_id)
            await queries_to_db.Friends.del_request_from_me(sender_id=sender_id, addressee_id=addressee_id)
            await queries_to_db.Friends.del_request_for_me(sender_id=sender_id, addressee_id=addressee_id)
        else:
            await queries_to_db.Friends.add_request_from_me(sender_id=sender_id, addressee_id=addressee_id)
            await queries_to_db.Friends.add_request_for_me(sender_id=sender_id, addressee_id=addressee_id)
        return True

    @staticmethod
    async def add_black_list(sender_id: int, addressee_id: int) -> Optional[bool]:
        if not await queries_to_db.User.check(telegram_id=addressee_id):
            return None
        if sender_id == addressee_id:
            return False
        if await queries_to_db.Friends.check_black_list(sender_id=sender_id, addressee_id=addressee_id):
            return False
        if await queries_to_db.Friends.check_friend(friend1=sender_id, friend2=addressee_id):
            await queries_to_db.Friends.del_friend(sender_id=sender_id, addressee_id=addressee_id)
        if await queries_to_db.Friends.check_request_from_me(sender_id=sender_id, addressee_id=addressee_id):
            await queries_to_db.Friends.del_request_from_me(sender_id=sender_id, addressee_id=addressee_id)
            await queries_to_db.Friends.del_request_for_me(sender_id=sender_id, addressee_id=addressee_id)
        await queries_to_db.Friends.add_black_list(sender_id=sender_id, addressee_id=addressee_id)
        return True

    @staticmethod
    async def del_friend(sender_id: int, addressee_id: int) -> bool:
        if await queries_to_db.Friends.check_friend(friend1=sender_id, friend2=addressee_id):
            await queries_to_db.Friends.del_friend(sender_id=sender_id, addressee_id=addressee_id)
            await queries_to_db.Friends.add_request_from_me(sender_id=sender_id, addressee_id=addressee_id)
            await queries_to_db.Friends.add_request_for_me(sender_id=sender_id, addressee_id=addressee_id)
            return True
        if await queries_to_db.Friends.check_request_from_me(sender_id=sender_id, addressee_id=addressee_id):
            await queries_to_db.Friends.del_request_from_me(sender_id=sender_id, addressee_id=addressee_id)
            await queries_to_db.Friends.del_request_for_me(sender_id=sender_id, addressee_id=addressee_id)
            return True
        return False

    @staticmethod
    async def del_black_list(sender_id: int, addressee_id: int) -> bool:
        if await queries_to_db.Friends.check_black_list(sender_id=sender_id, addressee_id=addressee_id):
            return False
        await queries_to_db.Friends.del_black_list(sender_id=sender_id, addressee_id=addressee_id)
        return True

    @staticmethod
    async def show_friends(telegram_id: int) -> Optional[list[int]]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.Friends.show_friends(telegram_id=telegram_id)

    @staticmethod
    async def show_friends_request_for_me(telegram_id: int) -> Optional[list[int]]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.Friends.show_friends_request_for_me(telegram_id=telegram_id)

    @staticmethod
    async def show_friends_request_from_me(telegram_id: int) -> Optional[list[int]]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.Friends.show_friends_request_from_me(telegram_id=telegram_id)

    @staticmethod
    async def show_black_list(telegram_id: int) -> Optional[list[int]]:
        if not await queries_to_db.User.check(telegram_id=telegram_id):
            return None
        return await queries_to_db.Friends.show_black_list(telegram_id=telegram_id)


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
    async def del_(variant_id: int) -> Optional[bool]:
        if not queries_to_db.Variant.check(variant_id=variant_id):
            return None
        await queries_to_db.Variant.del_(variant_id=variant_id)
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
