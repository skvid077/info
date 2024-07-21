import datetime

from typing import Optional

from pydantic import BaseModel

from schemas.s_enumeration import Complexity


class User(BaseModel):
    telegram_id: Optional[int]
    username: Optional[str]
    cash: Optional[int]
    is_admin: Optional[bool]


class User_tasks(User):
    tasks: list['Task'] = []


class User_friends(User):
    friends: list['User'] = []


class User_friends_request_from_me(User):
    friends_request_from_me: list['User'] = []


class User_friends_request_for_me(User):
    friends_request_for_me: list['User'] = []


class User_variants(User):
    variants: list['Variant'] = []


class Task(BaseModel):
    id: Optional[int]
    author_id: Optional[int]
    num: Optional[int]
    ans: Optional[str]
    extend_ans: Optional[str]
    verif: Optional[bool]
    complexity: Optional[Complexity]
    at_create: Optional[datetime.datetime]


class Variant(BaseModel):
    id: int
    author_id: int
    files: Optional[str]
    ans: Optional[str]
    at_create: Optional[datetime.datetime]
    verif: Optional[bool]
    tasks: list['Task'] = []
