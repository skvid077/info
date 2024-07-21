import datetime

from typing import TypedDict, NotRequired

from schemas.s_pydantic import Complexity


class User(TypedDict):
    telegram_id: int
    username: NotRequired[str]
    cash: NotRequired[int]
    is_admin: NotRequired[bool]


class Task(TypedDict):
    id: NotRequired[int]
    author_id: NotRequired[int]
    num: NotRequired[int]
    ans: NotRequired[str]
    extend_ans: NotRequired[str]
    verif: NotRequired[bool]
    complexity: NotRequired[Complexity]
    at_create: NotRequired[datetime.datetime]


class Variant(TypedDict):
    id: NotRequired[int]
    author_id: NotRequired[int]
    files: NotRequired[str]
    ans: NotRequired[str]
    complexity: NotRequired[Complexity]
    at_create: NotRequired[datetime.datetime]
    verif: NotRequired[bool]
