from typing import Optional

from database.queries import queries_to_db


class Friends:
    @staticmethod
    async def add_friend(sender_id: int, addressee_id: int) -> Optional[bool]:
        if not await queries_to_db.User.check(telegram_id=addressee_id):
            return None
        if not await queries_to_db.User.check(telegram_id=sender_id):
            return False
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
