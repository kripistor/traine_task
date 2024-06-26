from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

auth_async_engine = create_async_engine(
    str(settings.ASYNC_DATABASE_URL), pool_pre_ping=True
)

async_session_maker = async_sessionmaker(
    auth_async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    id: Any
