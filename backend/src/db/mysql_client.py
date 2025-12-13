import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy.exc import DBAPIError, OperationalError
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool

from ..conf import settings

TRANSIENT_MYSQL_ERRNOS = {1205, 1213, 2006, 2013}


def is_transient_mysql_error(e: Exception) -> bool:
    if isinstance(e, (OperationalError, DBAPIError)) and getattr(e, "orig", None):
        errno = getattr(e.orig, "args", [None])[0]
        return errno in TRANSIENT_MYSQL_ERRNOS
    return False


engine: AsyncEngine = create_async_engine(
    url=settings.mysql.dsn.unicode_string(),
    poolclass=AsyncAdaptedQueuePool,
    pool_size=settings.mysql.pool_size,
    max_overflow=settings.mysql.max_overflow,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    isolation_level=settings.mysql.isolation_level,
    connect_args={"connect_timeout": settings.mysql.connect_timeout},
    echo=settings.debug,
    future=True,
)


@asynccontextmanager
async def connection(retries: Optional[int] = 3) -> AsyncGenerator[AsyncConnection]:
    delay = 0.05
    retries = retries or 1

    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                yield conn
            return
        except Exception as exc:
            if attempt == retries - 1 or not is_transient_mysql_error(exc):
                raise
            await asyncio.sleep(delay)
            delay *= 2
