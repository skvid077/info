from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String

from database.config import settings

from typing import Annotated

async_engine = create_async_engine(url=settings.database_url)
async_session_factory = async_sessionmaker(async_engine)
str_50 = Annotated[str, 50]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_50: String(50)
    }
