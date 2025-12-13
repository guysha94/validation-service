from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..conf import settings

engine: AsyncEngine = create_async_engine(
    url=settings.sqlite.url,
    poolclass=AsyncAdaptedQueuePool,
    echo=settings.debug,
    future=True,
)


async def init_db():
    async with engine.begin() as conn:
        # Use run_sync for synchronous table creation
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(engine) as session:
        yield session
