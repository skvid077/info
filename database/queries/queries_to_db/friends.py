import json
import os

from database.json_models import get_path as get_path_json_models


class Friends:

    @staticmethod
    async def read() -> dict[int, dict[str, list[int]]]:
        with open(file=os.path.join(get_path_json_models(), 'friends.json'), mode='r', encoding='utf-8') as f:
            data: dict[int, dict[str, list[int]]] = {int(key): value for key, value in json.loads(f.read()).items()}
        await Friends.write(data)
        return data

    @staticmethod
    async def write(data: dict[int, dict[str, list[int]]]):
        with open(file=os.path.join(get_path_json_models(), 'friends.json'), mode='w', encoding='utf-8') as f:
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
