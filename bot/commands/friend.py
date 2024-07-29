from typing import Optional

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandObject
import keyboards
from database.queries import queries
from aiogram.fsm.context import FSMContext
from schemas import s_enumeration, s_pydantic


async def add_friend(msg: Message, command: CommandObject):
    if len(command.args.split()) != 1:
        await msg.answer(text='Неправильно переданы аргументы')
    if await queries.Friends.add_friend(sender_id=msg.from_user.id, addressee_id=int(command.args.split()[0])):
        await msg.answer(text='Друг добавлен')
    else:
        await msg.answer(text='Ошибка добавления')


async def del_friend(msg: Message, command: CommandObject):
    if len(command.args.split()) != 1:
        await msg.answer(text='Неправильно переданы аргументы')
    if await queries.Friends.del_friend(sender_id=msg.from_user.id, addressee_id=int(command.args.split()[0])):
        await msg.answer(text='Друг удалён')
    else:
        await msg.answer(text='Ошибка удаления')


async def add_black_list(msg: Message, command: CommandObject):
    if len(command.args.split()) != 1:
        await msg.answer(text='Неправильно переданы аргументы')
    if await queries.Friends.add_friend(sender_id=msg.from_user.id, addressee_id=int(command.args.split()[0])):
        await msg.answer(text='Пользователь добавлен в чёрный список')
    else:
        await msg.answer(text='Ошибка добавления')


async def del_black_list(msg: Message, command: CommandObject):
    if len(command.args.split()) != 1:
        await msg.answer(text='Неправильно переданы аргументы')
    if await queries.Friends.del_friend(sender_id=msg.from_user.id, addressee_id=int(command.args.split()[0])):
        await msg.answer(text='Пользователь удалён из чёрного списка')
    else:
        await msg.answer(text='Ошибка удаления')


async def show_friends(msg: Message):
    res: Optional[list[s_pydantic.User]] = await queries.User.show_friends(
        telegram_id=msg.from_user.id
    )
    if len(res) == 0:
        await msg.answer(text='Друзей нет')
        return
    res: list[str] = [f'-{i}) {friend.username} cash: {friend.cash} is_admin: {friend.is_admin}'
                      for i, friend in enumerate(res, 1)]
    text: str = 'Ваши Друзья:\n\n' + '\n'.join(res)
    await msg.answer(text=text)


async def show_friends_request_for_me(msg: Message):
    res: Optional[list[s_pydantic.User]] = await queries.User.show_friends_request_for_me(
        telegram_id=msg.from_user.id
    )
    if len(res) == 0:
        await msg.answer(text='Входящих заявок в друзья нет')
        return
    res: list[str] = [f'-{i}) {friend.username} cash: {friend.cash} is_admin: {friend.is_admin}'
                      for i, friend in enumerate(res, 1)]
    text: str = 'Входящие заявки в друзья:\n\n' + '\n'.join(res)
    await msg.answer(text=text)


async def show_friends_request_from_me(msg: Message):
    res: Optional[list[s_pydantic.User]] = await queries.User.show_friends_request_from_me(
        telegram_id=msg.from_user.id
    )
    if len(res) == 0:
        await msg.answer(text='Исходящих заявок в друзья нет')
        return
    res: list[str] = [f'-{i}) {friend.username} cash: {friend.cash} is_admin: {friend.is_admin}' for
                      i, friend in enumerate(res, 1)]
    text: str = 'Исходящие заявки в друзья:\n\n' + '\n'.join(res)
    await msg.answer(text=text)


async def show_black_list(msg: Message):
    res: Optional[list[s_pydantic.User]] = await queries.User.show_black_list(
        telegram_id=msg.from_user.id
    )
    if len(res) == 0:
        await msg.answer(text='Пользователей нет в чёрном списке')
        return
    res: list[str] = [f'-{i}) {friend.username} cash: {friend.cash} is_admin: {friend.is_admin}' for
                      i, friend in enumerate(res, 1)]
    text: str = 'Исходящие заявки в друзья:\n\n' + '\n'.join(res)
    await msg.answer(text=text)
