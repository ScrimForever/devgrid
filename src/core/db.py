from typing import AsyncGenerator
from fastapi import Depends
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = (
    f'postgresql+asyncpg://{os.getenv("POSTGRESQL_USERNAME")}:'
    f'{os.getenv("POSTGRESQL_PASSWORD")}@{os.getenv("POSTGRESQL_NAME")}/'
    f'{os.getenv("POSTGRESQL_DATABASE")}'
)


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_session(session: AsyncSession = Depends(get_async_session)):
    yield session
